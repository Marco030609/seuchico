// Configurações da API
const API_BASE = '/api';

// Estado da aplicação
let servicos = [];
let horariosDisponiveis = [];

// Elementos DOM
const servicosGrid = document.getElementById('servicos-grid');
const agendamentoForm = document.getElementById('agendamento-form');
const servicoSelect = document.getElementById('servico');
const dataInput = document.getElementById('data');
const horarioSelect = document.getElementById('horario');
const successModal = document.getElementById('success-modal');
const errorModal = document.getElementById('error-modal');
const errorMessage = document.getElementById('error-message');
const loading = document.getElementById('loading');

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    carregarServicos();
    configurarEventos();
    configurarDataMinima();
    configurarMascaraTelefone();
});

// Carregar serviços da API
async function carregarServicos() {
    try {
        const response = await fetch(`${API_BASE}/servicos`);
        const data = await response.json();
        
        if (data.success) {
            servicos = data.servicos;
            renderizarServicos();
            preencherSelectServicos();
        } else {
            console.error('Erro ao carregar serviços:', data.error);
        }
    } catch (error) {
        console.error('Erro na requisição:', error);
    }
}

// Renderizar serviços na grid
function renderizarServicos() {
    servicosGrid.innerHTML = '';
    
    servicos.forEach(servico => {
        const serviceCard = document.createElement('div');
        serviceCard.className = 'service-card';
        
        // Ícones para cada tipo de serviço
        let icon = 'fas fa-cut';
        if (servico.nome.toLowerCase().includes('barba')) {
            icon = 'fas fa-user-tie';
        } else if (servico.nome.toLowerCase().includes('combo')) {
            icon = 'fas fa-star';
        }
        
        serviceCard.innerHTML = `
            <div class="service-icon">
                <i class="${icon}"></i>
            </div>
            <h3 class="service-name">${servico.nome}</h3>
            <div class="service-price">R$ ${servico.preco.toFixed(2)}</div>
            <div class="service-duration">${servico.duracao_minutos} minutos</div>
        `;
        
        servicosGrid.appendChild(serviceCard);
    });
}

// Preencher select de serviços
function preencherSelectServicos() {
    servicoSelect.innerHTML = '<option value="">Selecione um serviço</option>';
    
    servicos.forEach(servico => {
        const option = document.createElement('option');
        option.value = servico.id;
        option.textContent = `${servico.nome} - R$ ${servico.preco.toFixed(2)}`;
        servicoSelect.appendChild(option);
    });
}

// Configurar eventos
function configurarEventos() {
    // Evento de mudança na data
    dataInput.addEventListener('change', carregarHorariosDisponiveis);
    
    // Evento de submissão do formulário
    agendamentoForm.addEventListener('submit', handleSubmitAgendamento);
    
    // Eventos de navegação
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = this.getAttribute('href').substring(1);
            scrollToSection(target);
            
            // Atualizar link ativo
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });
}

// Configurar data mínima (hoje)
function configurarDataMinima() {
    const hoje = new Date();
    const dataMinima = hoje.toISOString().split('T')[0];
    dataInput.min = dataMinima;
}

// Configurar máscara de telefone
function configurarMascaraTelefone() {
    const telefoneInput = document.getElementById('cliente-contato');
    
    telefoneInput.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, '');
        
        if (value.length <= 11) {
            if (value.length <= 2) {
                value = value.replace(/(\d{0,2})/, '($1');
            } else if (value.length <= 7) {
                value = value.replace(/(\d{2})(\d{0,5})/, '($1) $2');
            } else {
                value = value.replace(/(\d{2})(\d{5})(\d{0,4})/, '($1) $2-$3');
            }
        }
        
        e.target.value = value;
    });
}

// Carregar horários disponíveis
async function carregarHorariosDisponiveis() {
    const dataInput_value = dataInput.value;
    const servicoId = servicoSelect.value;
    
    if (!dataInput_value) {
        horarioSelect.disabled = true;
        horarioSelect.innerHTML = '<option value="">Selecione primeiro a data</option>';
        return;
    }
    
    // Converter data de YYYY-MM-DD para DD/MM/YYYY
    const [ano, mes, dia] = dataInput_value.split('-');
    const data = `${dia}/${mes}/${ano}`;
    
    try {
        horarioSelect.disabled = true;
        horarioSelect.innerHTML = '<option value="">Carregando horários...</option>';
        
        const params = new URLSearchParams({ data });
        if (servicoId) params.append('servico_id', servicoId);
        
        const response = await fetch(`${API_BASE}/horarios-disponiveis?${params}`);
        const responseData = await response.json();
        
        if (responseData.success) {
            horariosDisponiveis = responseData.horarios_disponiveis;
            preencherSelectHorarios();
        } else {
            horarioSelect.innerHTML = '<option value="">Erro ao carregar horários</option>';
            if (responseData.message) {
                horarioSelect.innerHTML = `<option value="">${responseData.message}</option>`;
            }
        }
    } catch (error) {
        console.error('Erro ao carregar horários:', error);
        horarioSelect.innerHTML = '<option value="">Erro ao carregar horários</option>';
    }
}

// Preencher select de horários
function preencherSelectHorarios() {
    horarioSelect.innerHTML = '';
    
    if (horariosDisponiveis.length === 0) {
        horarioSelect.innerHTML = '<option value="">Nenhum horário disponível</option>';
        horarioSelect.disabled = true;
        return;
    }
    
    horarioSelect.innerHTML = '<option value="">Selecione um horário</option>';
    
    horariosDisponiveis.forEach(horario => {
        const option = document.createElement('option');
        option.value = horario;
        option.textContent = horario;
        horarioSelect.appendChild(option);
    });
    
    horarioSelect.disabled = false;
}

// Handle submissão do agendamento
async function handleSubmitAgendamento(e) {
    e.preventDefault();
    
    const formData = new FormData(agendamentoForm);
    const dados = Object.fromEntries(formData.entries());
    
    // Validações
    if (!validarFormulario(dados)) {
        return;
    }
    
    // Converter dados
    dados.servico_id = parseInt(dados.servico_id);
    
    try {
        mostrarLoading(true);
        
        const response = await fetch(`${API_BASE}/agendar`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dados)
        });
        
        const result = await response.json();
        
        if (result.success) {
            mostrarModalSucesso();
            agendamentoForm.reset();
            configurarDataMinima();
            horarioSelect.disabled = true;
            horarioSelect.innerHTML = '<option value="">Selecione primeiro a data</option>';
        } else {
            mostrarModalErro(result.error || 'Erro ao realizar agendamento');
        }
    } catch (error) {
        console.error('Erro na requisição:', error);
        mostrarModalErro('Erro de conexão. Tente novamente.');
    } finally {
        mostrarLoading(false);
    }
}

// Validar formulário
function validarFormulario(dados) {
    // Validar nome
    if (!dados.cliente_nome || dados.cliente_nome.trim().length < 2) {
        mostrarModalErro('Nome deve ter pelo menos 2 caracteres');
        return false;
    }
    
    // Validar telefone
    const telefone = dados.cliente_contato.replace(/\D/g, '');
    if (telefone.length < 10 || telefone.length > 11) {
        mostrarModalErro('Telefone deve ter 10 ou 11 dígitos');
        return false;
    }
    
    // Validar email (se fornecido)
    if (dados.cliente_email && !isValidEmail(dados.cliente_email)) {
        mostrarModalErro('E-mail inválido');
        return false;
    }
    
    // Validar serviço
    if (!dados.servico_id) {
        mostrarModalErro('Selecione um serviço');
        return false;
    }
    
    // Validar data
    if (!dados.data_agendamento) {
        mostrarModalErro('Selecione uma data');
        return false;
    }
    
    // Validar horário
    if (!dados.hora_agendamento) {
        mostrarModalErro('Selecione um horário');
        return false;
    }
    
    return true;
}

// Validar email
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Mostrar/ocultar loading
function mostrarLoading(show) {
    if (show) {
        loading.style.display = 'flex';
    } else {
        loading.style.display = 'none';
    }
}

// Mostrar modal de sucesso
function mostrarModalSucesso() {
    successModal.style.display = 'block';
}

// Mostrar modal de erro
function mostrarModalErro(mensagem) {
    errorMessage.textContent = mensagem;
    errorModal.style.display = 'block';
}

// Fechar modal
function closeModal() {
    successModal.style.display = 'none';
    errorModal.style.display = 'none';
}

// Scroll suave para seção
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        const headerHeight = document.querySelector('.header').offsetHeight;
        const sectionTop = section.offsetTop - headerHeight - 20;
        
        window.scrollTo({
            top: sectionTop,
            behavior: 'smooth'
        });
    }
}

// Fechar modal ao clicar fora
window.addEventListener('click', function(e) {
    if (e.target === successModal || e.target === errorModal) {
        closeModal();
    }
});

// Fechar modal com ESC
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeModal();
    }
});

// Atualizar link ativo baseado no scroll
window.addEventListener('scroll', function() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');
    
    let current = '';
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop - 100;
        const sectionHeight = section.offsetHeight;
        
        if (window.scrollY >= sectionTop && window.scrollY < sectionTop + sectionHeight) {
            current = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
});

// Função global para o botão CTA
window.scrollToSection = scrollToSection;

