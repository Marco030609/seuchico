from datetime import datetime
from src.models.barbearia import Configuracao

def enviar_mensagem_whatsapp(numero, mensagem):
    """
    Simula o envio de mensagem via WhatsApp
    Em produção, integrar com API real como Twilio, ClickSend, etc.
    """
    try:
        # Por enquanto, apenas log da mensagem que seria enviada
        print(f"📱 WHATSAPP SIMULADO")
        print(f"Para: {numero}")
        print(f"Mensagem: {mensagem}")
        print(f"Enviado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("-" * 50)
        
        # Aqui seria a integração real com a API do WhatsApp
        # Exemplo com Twilio:
        # from twilio.rest import Client
        # client = Client(account_sid, auth_token)
        # message = client.messages.create(
        #     body=mensagem,
        #     from_='whatsapp:+14155238886',
        #     to=f'whatsapp:+55{numero}'
        # )
        
        return True
    except Exception as e:
        print(f"Erro ao enviar WhatsApp: {e}")
        return False

def notificar_novo_agendamento(agendamento):
    """Envia notificações para cliente e barbeiro sobre novo agendamento"""
    
    # Mensagem para o cliente
    mensagem_cliente = f"""
🎉 *Agendamento Confirmado!*

Olá {agendamento.cliente_nome}!

Seu agendamento foi realizado com sucesso:

📅 *Data:* {agendamento.data_agendamento.strftime('%d/%m/%Y')}
🕐 *Horário:* {agendamento.hora_agendamento.strftime('%H:%M')}
✂️ *Serviço:* {agendamento.servico.nome}
💰 *Valor:* R$ {agendamento.servico.preco:.2f}

📍 *Local:* Barbearia do Seu Chico

Em caso de dúvidas ou necessidade de reagendamento, entre em contato conosco.

Obrigado pela preferência! 🙏
    """.strip()
    
    # Enviar para o cliente
    cliente_numero = agendamento.cliente_contato.replace('(', '').replace(')', '').replace(' ', '').replace('-', '')
    enviar_mensagem_whatsapp(cliente_numero, mensagem_cliente)
    
    # Mensagem para o Seu Chico
    whatsapp_config = Configuracao.query.filter_by(chave='whatsapp_numero').first()
    if whatsapp_config:
        mensagem_barbeiro = f"""
🔔 *Novo Agendamento!*

👤 *Cliente:* {agendamento.cliente_nome}
📞 *Contato:* {agendamento.cliente_contato}
📅 *Data:* {agendamento.data_agendamento.strftime('%d/%m/%Y')}
🕐 *Horário:* {agendamento.hora_agendamento.strftime('%H:%M')}
✂️ *Serviço:* {agendamento.servico.nome}
💰 *Valor:* R$ {agendamento.servico.preco:.2f}

{f"📧 *Email:* {agendamento.cliente_email}" if agendamento.cliente_email else ""}
{f"📝 *Observações:* {agendamento.observacoes}" if agendamento.observacoes else ""}

Agendamento realizado em: {agendamento.data_criacao.strftime('%d/%m/%Y %H:%M:%S')}
        """.strip()
        
        enviar_mensagem_whatsapp(whatsapp_config.valor, mensagem_barbeiro)

def notificar_mudanca_status(agendamento, status_anterior):
    """Notifica sobre mudança de status do agendamento"""
    
    status_messages = {
        'confirmado': '✅ Seu agendamento foi confirmado!',
        'concluido': '🎉 Obrigado pela visita! Esperamos você novamente em breve.',
        'cancelado': '❌ Seu agendamento foi cancelado. Entre em contato para reagendar.'
    }
    
    if agendamento.status in status_messages:
        mensagem = f"""
{status_messages[agendamento.status]}

👤 *Cliente:* {agendamento.cliente_nome}
📅 *Data:* {agendamento.data_agendamento.strftime('%d/%m/%Y')}
🕐 *Horário:* {agendamento.hora_agendamento.strftime('%H:%M')}
✂️ *Serviço:* {agendamento.servico.nome}

*Barbearia do Seu Chico*
        """.strip()
        
        cliente_numero = agendamento.cliente_contato.replace('(', '').replace(')', '').replace(' ', '').replace('-', '')
        enviar_mensagem_whatsapp(cliente_numero, mensagem)

def enviar_relatorio_semanal():
    """Envia relatório semanal para o Seu Chico"""
    # Esta função seria chamada por um cron job
    pass

def enviar_relatorio_mensal():
    """Envia relatório mensal para o Seu Chico"""
    # Esta função seria chamada por um cron job
    pass

