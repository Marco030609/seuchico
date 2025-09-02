import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.models.barbearia import Servico, HorarioFuncionamento, Configuracao
from src.routes.user import user_bp
from src.routes.agendamento import agendamento_bp
from src.routes.admin import admin_bp
from datetime import time

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Configurar CORS para permitir requisições do frontend
CORS(app)

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(agendamento_bp, url_prefix='/api')
app.register_blueprint(admin_bp)

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def criar_dados_iniciais():
    """Cria dados iniciais se não existirem"""
    # Verificar se já existem serviços
    if Servico.query.count() == 0:
        # Criar serviços baseados nas informações fornecidas
        servicos = [
            Servico(nome='Barba', preco=35.00, duracao_minutos=30),
            Servico(nome='Cabelo', preco=35.00, duracao_minutos=45),
            Servico(nome='Combo (Cabelo + Barba)', preco=60.00, duracao_minutos=60)
        ]
        
        for servico in servicos:
            db.session.add(servico)
    
    # Verificar se já existem horários de funcionamento
    if HorarioFuncionamento.query.count() == 0:
        # Criar horários de funcionamento (Segunda a Sábado, 8h às 18h)
        horarios = [
            HorarioFuncionamento(dia_semana=0, hora_inicio=time(8, 0), hora_fim=time(18, 0)),  # Segunda
            HorarioFuncionamento(dia_semana=1, hora_inicio=time(8, 0), hora_fim=time(18, 0)),  # Terça
            HorarioFuncionamento(dia_semana=2, hora_inicio=time(8, 0), hora_fim=time(18, 0)),  # Quarta
            HorarioFuncionamento(dia_semana=3, hora_inicio=time(8, 0), hora_fim=time(18, 0)),  # Quinta
            HorarioFuncionamento(dia_semana=4, hora_inicio=time(8, 0), hora_fim=time(18, 0)),  # Sexta
            HorarioFuncionamento(dia_semana=5, hora_inicio=time(8, 0), hora_fim=time(18, 0)),  # Sábado
        ]
        
        for horario in horarios:
            db.session.add(horario)
    
    # Criar configurações iniciais
    if Configuracao.query.count() == 0:
        configuracoes = [
            Configuracao(chave='whatsapp_numero', valor='5511999656990', descricao='Número do WhatsApp do Seu Chico'),
            Configuracao(chave='email_admin', valor='seuchicobarbearia@gmail.com', descricao='Email do administrador'),
            Configuracao(chave='nome_barbearia', valor='Barbearia do Seu Chico', descricao='Nome da barbearia'),
            Configuracao(chave='endereco', valor='Endereço da barbearia', descricao='Endereço completo'),
        ]
        
        for config in configuracoes:
            db.session.add(config)
    
    db.session.commit()

with app.app_context():
    db.create_all()
    criar_dados_iniciais()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
