# 🔧 Barbearia do Seu Chico - Sistema de Agendamento Online

Sistema profissional de agendamento online para a Barbearia do Seu Chico, com design minimalista, sistema inteligente de horários e painel administrativo completo.

## 🌐 Site em Produção

**URL Principal:** https://8xhpiqclzxom.manus.space
**Painel Administrativo:** https://8xhpiqclzxom.manus.space/admin

## ✨ Funcionalidades

### 🎯 Para Clientes
- **Design Minimalista e Profissional** com cores neutras e escuras
- **Agendamento Intuitivo** com formulário simples e validado
- **Sistema Inteligente** que bloqueia horários passados e ocupados
- **Notificações WhatsApp** automáticas após agendamento
- **Responsivo** para desktop e mobile
- **Máscara automática** para telefone

### 🔧 Para o Seu Chico (Painel Administrativo)
- **Dashboard Completo** com estatísticas em tempo real
- **Gestão de Agendamentos** com controle de status
- **Filtros Avançados** por data e status
- **Notificações WhatsApp** para novos agendamentos
- **Relatórios** de faturamento e horas trabalhadas

## 📋 Serviços Disponíveis

| Serviço | Preço | Duração |
|---------|-------|---------|
| Barba | R$ 35,00 | 30 min |
| Cabelo | R$ 35,00 | 45 min |
| Combo (Cabelo + Barba) | R$ 60,00 | 60 min |

## 🕐 Horário de Funcionamento

**Segunda a Sábado:** 8h às 18h
**Domingo:** Fechado

## 📱 Contatos

- **WhatsApp:** (11) 99965-6990
- **Instagram:** @seuchicobarbearia4
- **Endereço:** Barbearia do Seu Chico

## 🔐 Acesso Administrativo

### Login do Painel
- **URL:** https://8xhpiqclzxom.manus.space/admin/login
- **Usuário:** seuchico
- **Senha:** barbearia2024

### Funcionalidades do Painel
1. **Estatísticas em Tempo Real**
   - Total de agendamentos
   - Atendimentos realizados
   - Faturamento total
   - Horas trabalhadas
   - Agendamentos do dia

2. **Gestão de Agendamentos**
   - Visualizar todos os agendamentos
   - Alterar status (Pendente → Confirmado → Concluído)
   - Filtrar por data e status
   - Cancelar agendamentos

3. **Notificações Automáticas**
   - Cliente recebe confirmação via WhatsApp
   - Seu Chico recebe notificação de novos agendamentos
   - Notificações de mudança de status

## 🚀 Tecnologias Utilizadas

- **Backend:** Flask (Python)
- **Frontend:** HTML5, CSS3, JavaScript
- **Banco de Dados:** SQLite
- **Notificações:** Sistema WhatsApp simulado (pronto para integração real)
- **Deploy:** Manus Platform

## 📱 Sistema de Notificações WhatsApp

O sistema está configurado para enviar notificações automáticas:

### Para o Cliente:
```
🎉 Agendamento Confirmado!

Olá [Nome]!

Seu agendamento foi realizado com sucesso:

📅 Data: [Data]
🕐 Horário: [Horário]
✂️ Serviço: [Serviço]
💰 Valor: R$ [Valor]

📍 Local: Barbearia do Seu Chico

Obrigado pela preferência! 🙏
```

### Para o Seu Chico:
```
🔔 Novo Agendamento!

👤 Cliente: [Nome]
📞 Contato: [WhatsApp]
📅 Data: [Data]
🕐 Horário: [Horário]
✂️ Serviço: [Serviço]
💰 Valor: R$ [Valor]
```

## 🔧 Configuração para Produção

### Integração WhatsApp Real
Para ativar notificações WhatsApp reais, integre com:
- **Twilio API**
- **ClickSend**
- **WhatsApp Business API**

### Relatórios Automáticos
O sistema está preparado para enviar:
- **Relatórios semanais** (todo domingo)
- **Relatórios mensais** (último dia do mês)

## 📊 Fluxo de Agendamento

1. **Cliente acessa o site**
2. **Preenche o formulário** com dados pessoais
3. **Seleciona serviço** e data
4. **Escolhe horário** disponível
5. **Confirma agendamento**
6. **Recebe notificação** WhatsApp
7. **Seu Chico recebe** notificação
8. **Painel administrativo** atualiza automaticamente

## 🎨 Design

- **Cores:** Neutras e escuras (preto, cinza, dourado)
- **Tipografia:** Inter (moderna e legível)
- **Layout:** Minimalista e intuitivo
- **Responsivo:** Funciona em todos os dispositivos

## 🔒 Segurança

- **Validações** de formulário no frontend e backend
- **Sanitização** de dados de entrada
- **Proteção** contra horários inválidos
- **Controle de acesso** ao painel administrativo

## 📈 Próximas Melhorias

- [ ] Integração com WhatsApp Business API real
- [ ] Sistema de pagamento online
- [ ] Agendamento recorrente
- [ ] Avaliações de clientes
- [ ] Programa de fidelidade
- [ ] Integração com Google Calendar

---

**Desenvolvido com ❤️ para a Barbearia do Seu Chico**
*Sistema profissional de agendamento online desde 2024*

