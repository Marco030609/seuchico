## Tarefas

### Fase 1: Análise dos requisitos e planejamento da arquitetura
- [ ] Detalhar os requisitos funcionais e não funcionais do site.
- [ ] Definir a arquitetura do sistema (frontend, backend, banco de dados).
- [ ] Planejar a estrutura do banco de dados para agendamentos e informações do Seu Chico.

### Fase 2: Criação da estrutura do projeto Flask
- [x] Criar um novo projeto Flask.
- [x] Configurar o ambiente de desenvolvimento.
- [x] Estruturar as pastas e arquivos do projeto.
- [x] Criar modelos para serviços, agendamentos, configurações e horários de funcionamento.
- [x] Criar rotas para o sistema de agendamento.
- [x] Configurar CORS e dependências.

### Fase 3: Desenvolvimento do frontend com design minimalista
- [x] Desenvolver a interface de agendamento (página inicial).
- [x] Implementar o design minimalista e intuitivo com cores neutras e escuras.
- [x] Adicionar a logo e informações da barbearia.
- [x] Criar a seção de serviços e preços.
- [x] Implementar formulário de agendamento funcional.
- [x] Testar responsividade e interações do usuári### Fase 4: Implementação do sistema de agendamento inteligente
- [x] Desenvolver a lógica para seleção de horários disponíveis.
- [x] Implementar validações de horários passados.
- [x] Criar sistema de bloqueio de horários ocupados.
- [x] Integrar notificações WhatsApp simuladas.
- [x] Corrigir bugs de formatação de data.
- [x] Testar funcionalidades do sistema de agendamento.o concluído.

### Fase 5: Criação do painel administrativo do Seu Chico
- [ ] Desenvolver a interface do painel administrativo.
- [ ] Implementar a visualização de agendamentos (atendidos, faturamento, horas trabalhadas, pessoas no dia).
- [ ] Criar a funcionalidade de resumo semanal e mensal por e-mail.

### Fase 6: Integração com WhatsApp e sistema de notificações
- [ ] Configurar a API de envio de mensagens para WhatsApp.
- [ ] Enviar confirmação de agendamento para o cliente via WhatsApp.
- [ ] Enviar informações do serviço, preço e horário para o WhatsApp do Seu Chico.

### Fase 7: Testes locais e ajustes finais
- [ ] Realizar testes funcionais de todas as funcionalidades.
- [ ] Testar a responsividade do site em diferentes dispositivos.
- [ ] Otimizar o desempenho do site.

### Fase 8: Deploy do site para produção
- [ ] Preparar o ambiente de produção.
- [ ] Realizar o deploy do frontend e backend.
- [ ] Configurar o domínio e SSL.



### Requisitos Detalhados

#### Requisitos Funcionais:
- Agendamento online de serviços (cabelo, barba, combo).
- Exibição dinâmica de horários disponíveis, considerando horários passados e já agendados.
- Coleta de nome, contato (email/WhatsApp) e tipo de serviço do cliente.
- Mensagem de confirmação 'agendamento concluído' após o agendamento.
- Sem redirecionamento para sites externos.
- Painel administrativo para 'Seu Chico' com:
    - Número de pessoas atendidas.
    - Faturamento total.
    - Horas trabalhadas.
    - Agendamentos diários.
- Envio de e-mails de resumo semanal e mensal para 'Seu Chico'.
- Envio de informações do serviço, preço e horário para o WhatsApp do cliente e do Seu Chico.

#### Requisitos Não Funcionais:
- **Design:** Minimalista, profissional, cores neutras e escuras, conforto visual, intuitivo.
- **Performance:** Rápido e responsivo.
- **Segurança:** Proteção de dados do cliente e do Seu Chico.
- **Usabilidade:** Botões intuitivos, página inteira intuitiva.

#### Arquitetura do Sistema:
- **Frontend:** HTML, CSS (com foco em design responsivo), JavaScript.
- **Backend:** Flask (Python).
- **Banco de Dados:** SQLite (para simplicidade inicial, pode ser migrado para PostgreSQL/MySQL se necessário).
- **Comunicação:** API para WhatsApp (Twilio, ClickSend ou similar, a ser pesquisado).

#### Estrutura do Banco de Dados (Proposta Inicial):
- **Tabela `servicos`:**
    - `id` (PK)
    - `nome` (TEXT)
    - `preco` (REAL)
- **Tabela `agendamentos`:**
    - `id` (PK)
    - `cliente_nome` (TEXT)
    - `cliente_contato` (TEXT)
    - `cliente_email` (TEXT)
    - `servico_id` (FK para `servicos`)
    - `data_agendamento` (DATE)
    - `hora_agendamento` (TIME)
    - `status` (TEXT: 'pendente', 'confirmado', 'concluido', 'cancelado')
    - `data_criacao` (DATETIME)
- **Tabela `configuracoes` (para dados do Seu Chico e faturamento):**
    - `id` (PK)
    - `chave` (TEXT)
    - `valor` (TEXT)



