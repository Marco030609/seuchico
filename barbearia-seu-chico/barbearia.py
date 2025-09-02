from src.models.user import db
from datetime import datetime

class Servico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    duracao_minutos = db.Column(db.Integer, nullable=False, default=30)
    ativo = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Servico {self.nome}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'preco': self.preco,
            'duracao_minutos': self.duracao_minutos,
            'ativo': self.ativo
        }

class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_nome = db.Column(db.String(100), nullable=False)
    cliente_contato = db.Column(db.String(20), nullable=False)
    cliente_email = db.Column(db.String(120), nullable=True)
    servico_id = db.Column(db.Integer, db.ForeignKey('servico.id'), nullable=False)
    data_agendamento = db.Column(db.Date, nullable=False)
    hora_agendamento = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default='pendente')  # pendente, confirmado, concluido, cancelado
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    observacoes = db.Column(db.Text, nullable=True)
    
    # Relacionamento
    servico = db.relationship('Servico', backref=db.backref('agendamentos', lazy=True))
    
    def __repr__(self):
        return f'<Agendamento {self.cliente_nome} - {self.data_agendamento}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'cliente_nome': self.cliente_nome,
            'cliente_contato': self.cliente_contato,
            'cliente_email': self.cliente_email,
            'servico': self.servico.to_dict() if self.servico else None,
            'data_agendamento': self.data_agendamento.isoformat() if self.data_agendamento else None,
            'hora_agendamento': self.hora_agendamento.strftime('%H:%M') if self.hora_agendamento else None,
            'status': self.status,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'observacoes': self.observacoes
        }

class Configuracao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chave = db.Column(db.String(100), unique=True, nullable=False)
    valor = db.Column(db.Text, nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<Configuracao {self.chave}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'chave': self.chave,
            'valor': self.valor,
            'descricao': self.descricao
        }

class HorarioFuncionamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dia_semana = db.Column(db.Integer, nullable=False)  # 0=Segunda, 1=Terça, ..., 6=Domingo
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fim = db.Column(db.Time, nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<HorarioFuncionamento {self.dia_semana}>'
    
    def to_dict(self):
        dias = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        return {
            'id': self.id,
            'dia_semana': self.dia_semana,
            'dia_nome': dias[self.dia_semana] if 0 <= self.dia_semana <= 6 else 'Desconhecido',
            'hora_inicio': self.hora_inicio.strftime('%H:%M') if self.hora_inicio else None,
            'hora_fim': self.hora_fim.strftime('%H:%M') if self.hora_fim else None,
            'ativo': self.ativo
        }

