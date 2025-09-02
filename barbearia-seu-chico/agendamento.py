from flask import Blueprint, request, jsonify
from datetime import datetime, date, time, timedelta
from src.models.barbearia import db, Servico, Agendamento, HorarioFuncionamento, Configuracao
from src.utils.whatsapp import notificar_novo_agendamento, notificar_mudanca_status
import json

agendamento_bp = Blueprint('agendamento', __name__)

@agendamento_bp.route('/servicos', methods=['GET'])
def listar_servicos():
    """Lista todos os serviços ativos"""
    try:
        servicos = Servico.query.filter_by(ativo=True).all()
        return jsonify({
            'success': True,
            'servicos': [servico.to_dict() for servico in servicos]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@agendamento_bp.route('/horarios-funcionamento', methods=['GET'])
def listar_horarios_funcionamento():
    """Lista os horários de funcionamento"""
    try:
        horarios = HorarioFuncionamento.query.filter_by(ativo=True).all()
        return jsonify({
            'success': True,
            'horarios': [horario.to_dict() for horario in horarios]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@agendamento_bp.route('/horarios-disponiveis', methods=['GET'])
def horarios_disponiveis():
    """Retorna horários disponíveis para uma data específica"""
    try:
        data_str = request.args.get('data')
        servico_id = request.args.get('servico_id', type=int)
        
        if not data_str:
            return jsonify({"success": False, "error": "Data é obrigatória"}), 400
        data_agendamento = datetime.strptime(data_str, 
            '%d/%m/%Y').date()
        if data_agendamento < date.today():
            return jsonify({'success': False, 'error': 'Não é possível agendar para datas passadas'}), 400
        
        # Obter dia da semana (0=Segunda, 6=Domingo)
        dia_semana = data_agendamento.weekday()
        
        # Buscar horário de funcionamento para o dia
        horario_funcionamento = HorarioFuncionamento.query.filter_by(
            dia_semana=dia_semana, 
            ativo=True
        ).first()
        
        if not horario_funcionamento:
            return jsonify({
                'success': True,
                'horarios_disponiveis': [],
                'message': 'Não funcionamos neste dia da semana'
            })
        
        # Gerar horários possíveis (de 30 em 30 minutos)
        horarios_possiveis = []
        hora_atual = datetime.combine(date.today(), horario_funcionamento.hora_inicio)
        hora_fim = datetime.combine(date.today(), horario_funcionamento.hora_fim)
        
        while hora_atual < hora_fim:
            horarios_possiveis.append(hora_atual.time())
            hora_atual += timedelta(minutes=30)
        
        # Buscar agendamentos já existentes para a data
        agendamentos_existentes = Agendamento.query.filter_by(
            data_agendamento=data_agendamento
        ).filter(Agendamento.status.in_(['pendente', 'confirmado'])).all()
        
        horarios_ocupados = [ag.hora_agendamento for ag in agendamentos_existentes]
        
        # Se for hoje, remover horários que já passaram
        if data_agendamento == date.today():
            hora_atual_hoje = datetime.now().time()
            horarios_possiveis = [h for h in horarios_possiveis if h > hora_atual_hoje]
        
        # Remover horários ocupados
        horarios_disponiveis = [h for h in horarios_possiveis if h not in horarios_ocupados]
        
        return jsonify({
            'success': True,
            'horarios_disponiveis': [h.strftime('%H:%M') for h in horarios_disponiveis]
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@agendamento_bp.route('/agendar', methods=['POST'])
def criar_agendamento():
    """Cria um novo agendamento"""
    try:
        dados = request.get_json()
        
        # Validar dados obrigatórios
        campos_obrigatorios = ['cliente_nome', 'cliente_contato', 'servico_id', 'data_agendamento', 'hora_agendamento']
        for campo in campos_obrigatorios:
            if not dados.get(campo):
                return jsonify({'success': False, 'error': f'Campo {campo} é obrigatório'}), 400
        
        # Converter data e hora
        data_agendamento = datetime.strptime(dados['data_agendamento'], '%Y-%m-%d').date()
        hora_agendamento = datetime.strptime(dados['hora_agendamento'], '%H:%M').time()
        
        # Verificar se a data não é no passado
        if data_agendamento < date.today():
            return jsonify({'success': False, 'error': 'Não é possível agendar para datas passadas'}), 400
        
        # Verificar se o horário ainda está disponível
        agendamento_existente = Agendamento.query.filter_by(
            data_agendamento=data_agendamento,
            hora_agendamento=hora_agendamento
        ).filter(Agendamento.status.in_(['pendente', 'confirmado'])).first()
        
        if agendamento_existente:
            return jsonify({'success': False, 'error': 'Este horário já está ocupado'}), 400
        
        # Verificar se o serviço existe
        servico = Servico.query.get(dados['servico_id'])
        if not servico:
            return jsonify({'success': False, 'error': 'Serviço não encontrado'}), 404
        
        # Criar agendamento
        agendamento = Agendamento(
            cliente_nome=dados['cliente_nome'],
            cliente_contato=dados['cliente_contato'],
            cliente_email=dados.get('cliente_email'),
            servico_id=dados['servico_id'],
            data_agendamento=data_agendamento,
            hora_agendamento=hora_agendamento,
            observacoes=dados.get('observacoes')
        )
        
        db.session.add(agendamento)
        db.session.commit()
        
        # Enviar notificações WhatsApp
        try:
            notificar_novo_agendamento(agendamento)
        except Exception as e:
            print(f"Erro ao enviar notificação WhatsApp: {e}")
        
        return jsonify({
            'success': True,
            'message': 'Agendamento realizado com sucesso!',
            'agendamento': agendamento.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@agendamento_bp.route('/agendamentos', methods=['GET'])
def listar_agendamentos():
    """Lista agendamentos (para o painel administrativo)"""
    try:
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')
        status = request.args.get('status')
        
        query = Agendamento.query
        
        if data_inicio:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            query = query.filter(Agendamento.data_agendamento >= data_inicio)
        
        if data_fim:
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
            query = query.filter(Agendamento.data_agendamento <= data_fim)
        
        if status:
            query = query.filter(Agendamento.status == status)
        
        agendamentos = query.order_by(Agendamento.data_agendamento.desc(), Agendamento.hora_agendamento.desc()).all()
        
        return jsonify({
            'success': True,
            'agendamentos': [agendamento.to_dict() for agendamento in agendamentos]
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@agendamento_bp.route('/agendamentos/<int:agendamento_id>/status', methods=['PUT'])
def atualizar_status_agendamento(agendamento_id):
    """Atualiza o status de um agendamento"""
    try:
        dados = request.get_json()
        novo_status = dados.get('status')
        
        if novo_status not in ['pendente', 'confirmado', 'concluido', 'cancelado']:
            return jsonify({'success': False, 'error': 'Status inválido'}), 400
        
        agendamento = Agendamento.query.get(agendamento_id)
        if not agendamento:
            return jsonify({'success': False, 'error': 'Agendamento não encontrado'}), 404
        
        status_anterior = agendamento.status
        agendamento.status = novo_status
        db.session.commit()
        
        # Enviar notificação sobre mudança de status
        try:
            notificar_mudanca_status(agendamento, status_anterior)
        except Exception as e:
            print(f"Erro ao enviar notificação WhatsApp: {e}")
        
        return jsonify({
            'success': True,
            'message': 'Status atualizado com sucesso',
            'agendamento': agendamento.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@agendamento_bp.route('/dashboard/estatisticas', methods=['GET'])
def estatisticas_dashboard():
    """Retorna estatísticas para o dashboard do Seu Chico"""
    try:
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')
        
        # Se não especificado, usar o mês atual
        if not data_inicio or not data_fim:
            hoje = date.today()
            data_inicio = date(hoje.year, hoje.month, 1)
            data_fim = hoje
        else:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
        
        # Agendamentos no período
        agendamentos = Agendamento.query.filter(
            Agendamento.data_agendamento >= data_inicio,
            Agendamento.data_agendamento <= data_fim
        ).all()
        
        # Estatísticas
        total_agendamentos = len(agendamentos)
        agendamentos_concluidos = len([a for a in agendamentos if a.status == 'concluido'])
        
        # Faturamento (apenas agendamentos concluídos)
        faturamento_total = sum([a.servico.preco for a in agendamentos if a.status == 'concluido'])
        
        # Horas trabalhadas (estimativa baseada na duração dos serviços concluídos)
        horas_trabalhadas = sum([a.servico.duracao_minutos for a in agendamentos if a.status == 'concluido']) / 60
        
        # Agendamentos de hoje
        agendamentos_hoje = len([a for a in agendamentos if a.data_agendamento == date.today()])
        
        return jsonify({
            'success': True,
            'estatisticas': {
                'total_agendamentos': total_agendamentos,
                'agendamentos_concluidos': agendamentos_concluidos,
                'faturamento_total': faturamento_total,
                'horas_trabalhadas': round(horas_trabalhadas, 2),
                'agendamentos_hoje': agendamentos_hoje,
                'periodo': {
                    'data_inicio': data_inicio.isoformat(),
                    'data_fim': data_fim.isoformat()
                }
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

