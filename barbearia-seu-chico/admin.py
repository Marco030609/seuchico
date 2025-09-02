from flask import Blueprint, request, jsonify, render_template_string
from datetime import datetime, date, timedelta
from src.models.barbearia import db, Servico, Agendamento, HorarioFuncionamento, Configuracao
from sqlalchemy import func, extract
import calendar

admin_bp = Blueprint('admin', __name__)

# Template HTML para o painel administrativo
ADMIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Painel Administrativo - Seu Chico</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background-color: #1a1a1a;
            color: #ffffff;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background-color: #2d2d2d;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 30px;
            text-align: center;
        }
        
        .header h1 {
            color: #d4af37;
            font-size: 2rem;
            margin-bottom: 10px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background-color: #2d2d2d;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #404040;
            text-align: center;
        }
        
        .stat-value {
            font-size: 2rem;
            font-weight: bold;
            color: #d4af37;
            margin-bottom: 5px;
        }
        
        .stat-label {
            color: #b0b0b0;
            font-size: 0.9rem;
        }
        
        .section {
            background-color: #2d2d2d;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 20px;
            border: 1px solid #404040;
        }
        
        .section h2 {
            color: #d4af37;
            margin-bottom: 20px;
            font-size: 1.5rem;
        }
        
        .table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .table th,
        .table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #404040;
        }
        
        .table th {
            background-color: #3a3a3a;
            color: #d4af37;
            font-weight: 600;
        }
        
        .status {
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: 500;
        }
        
        .status.pendente {
            background-color: #ffc107;
            color: #000;
        }
        
        .status.confirmado {
            background-color: #17a2b8;
            color: #fff;
        }
        
        .status.concluido {
            background-color: #28a745;
            color: #fff;
        }
        
        .status.cancelado {
            background-color: #dc3545;
            color: #fff;
        }
        
        .btn {
            padding: 8px 16px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9rem;
            margin: 2px;
        }
        
        .btn-success {
            background-color: #28a745;
            color: white;
        }
        
        .btn-danger {
            background-color: #dc3545;
            color: white;
        }
        
        .btn-info {
            background-color: #17a2b8;
            color: white;
        }
        
        .filters {
            margin-bottom: 20px;
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        .filters input,
        .filters select {
            padding: 8px 12px;
            border: 1px solid #404040;
            border-radius: 6px;
            background-color: #3a3a3a;
            color: #ffffff;
        }
        
        .refresh-btn {
            background-color: #d4af37;
            color: #1a1a1a;
            padding: 10px 20px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            margin-bottom: 20px;
        }
        
        .refresh-btn:hover {
            background-color: #b8941f;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔧 Painel Administrativo</h1>
            <p>Barbearia do Seu Chico</p>
        </div>
        
        <button class="refresh-btn" onclick="location.reload()">🔄 Atualizar Dados</button>
        
        <div class="stats-grid" id="stats-grid">
            <!-- Estatísticas serão carregadas aqui -->
        </div>
        
        <div class="section">
            <h2>📅 Agendamentos Recentes</h2>
            <div class="filters">
                <input type="date" id="data-inicio" placeholder="Data início">
                <input type="date" id="data-fim" placeholder="Data fim">
                <select id="status-filter">
                    <option value="">Todos os status</option>
                    <option value="pendente">Pendente</option>
                    <option value="confirmado">Confirmado</option>
                    <option value="concluido">Concluído</option>
                    <option value="cancelado">Cancelado</option>
                </select>
                <button class="btn btn-info" onclick="filtrarAgendamentos()">Filtrar</button>
            </div>
            <div id="agendamentos-container">
                <!-- Agendamentos serão carregados aqui -->
            </div>
        </div>
    </div>
    
    <script>
        // Carregar dados ao inicializar
        document.addEventListener('DOMContentLoaded', function() {
            carregarEstatisticas();
            carregarAgendamentos();
        });
        
        async function carregarEstatisticas() {
            try {
                const response = await fetch('/api/dashboard/estatisticas');
                const data = await response.json();
                
                if (data.success) {
                    const stats = data.estatisticas;
                    document.getElementById('stats-grid').innerHTML = `
                        <div class="stat-card">
                            <div class="stat-value">${stats.total_agendamentos}</div>
                            <div class="stat-label">Total de Agendamentos</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">${stats.agendamentos_concluidos}</div>
                            <div class="stat-label">Atendimentos Realizados</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">R$ ${stats.faturamento_total.toFixed(2)}</div>
                            <div class="stat-label">Faturamento Total</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">${stats.horas_trabalhadas}h</div>
                            <div class="stat-label">Horas Trabalhadas</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">${stats.agendamentos_hoje}</div>
                            <div class="stat-label">Agendamentos Hoje</div>
                        </div>
                    `;
                }
            } catch (error) {
                console.error('Erro ao carregar estatísticas:', error);
            }
        }
        
        async function carregarAgendamentos() {
            try {
                const response = await fetch('/api/agendamentos');
                const data = await response.json();
                
                if (data.success) {
                    renderizarAgendamentos(data.agendamentos);
                }
            } catch (error) {
                console.error('Erro ao carregar agendamentos:', error);
            }
        }
        
        function renderizarAgendamentos(agendamentos) {
            const container = document.getElementById('agendamentos-container');
            
            if (agendamentos.length === 0) {
                container.innerHTML = '<p>Nenhum agendamento encontrado.</p>';
                return;
            }
            
            const tabela = `
                <table class="table">
                    <thead>
                        <tr>
                            <th>Cliente</th>
                            <th>Contato</th>
                            <th>Serviço</th>
                            <th>Data</th>
                            <th>Horário</th>
                            <th>Status</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${agendamentos.map(agendamento => `
                            <tr>
                                <td>${agendamento.cliente_nome}</td>
                                <td>${agendamento.cliente_contato}</td>
                                <td>${agendamento.servico ? agendamento.servico.nome : 'N/A'}</td>
                                <td>${new Date(agendamento.data_agendamento).toLocaleDateString('pt-BR')}</td>
                                <td>${agendamento.hora_agendamento}</td>
                                <td><span class="status ${agendamento.status}">${agendamento.status}</span></td>
                                <td>
                                    ${agendamento.status === 'pendente' ? `
                                        <button class="btn btn-success" onclick="atualizarStatus(${agendamento.id}, 'confirmado')">Confirmar</button>
                                        <button class="btn btn-danger" onclick="atualizarStatus(${agendamento.id}, 'cancelado')">Cancelar</button>
                                    ` : ''}
                                    ${agendamento.status === 'confirmado' ? `
                                        <button class="btn btn-success" onclick="atualizarStatus(${agendamento.id}, 'concluido')">Concluir</button>
                                    ` : ''}
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
            
            container.innerHTML = tabela;
        }
        
        async function atualizarStatus(agendamentoId, novoStatus) {
            try {
                const response = await fetch(`/api/agendamentos/${agendamentoId}/status`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ status: novoStatus })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    alert('Status atualizado com sucesso!');
                    carregarAgendamentos();
                    carregarEstatisticas();
                } else {
                    alert('Erro ao atualizar status: ' + data.error);
                }
            } catch (error) {
                console.error('Erro ao atualizar status:', error);
                alert('Erro de conexão');
            }
        }
        
        async function filtrarAgendamentos() {
            const dataInicio = document.getElementById('data-inicio').value;
            const dataFim = document.getElementById('data-fim').value;
            const status = document.getElementById('status-filter').value;
            
            const params = new URLSearchParams();
            if (dataInicio) params.append('data_inicio', dataInicio);
            if (dataFim) params.append('data_fim', dataFim);
            if (status) params.append('status', status);
            
            try {
                const response = await fetch(`/api/agendamentos?${params}`);
                const data = await response.json();
                
                if (data.success) {
                    renderizarAgendamentos(data.agendamentos);
                }
            } catch (error) {
                console.error('Erro ao filtrar agendamentos:', error);
            }
        }
    </script>
</body>
</html>
"""

@admin_bp.route('/admin')
def painel_admin():
    """Página do painel administrativo"""
    return render_template_string(ADMIN_TEMPLATE)

@admin_bp.route('/admin/login')
def admin_login():
    """Página de login do admin (simplificada)"""
    # Por simplicidade, vamos apenas redirecionar para o painel
    # Em produção, implementar autenticação adequada
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login - Painel Administrativo</title>
        <style>
            body {
                font-family: 'Inter', sans-serif;
                background-color: #1a1a1a;
                color: #ffffff;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .login-container {
                background-color: #2d2d2d;
                padding: 40px;
                border-radius: 12px;
                border: 1px solid #404040;
                text-align: center;
                max-width: 400px;
                width: 100%;
            }
            .login-container h1 {
                color: #d4af37;
                margin-bottom: 30px;
            }
            .form-group {
                margin-bottom: 20px;
                text-align: left;
            }
            .form-group label {
                display: block;
                margin-bottom: 5px;
                color: #b0b0b0;
            }
            .form-group input {
                width: 100%;
                padding: 12px;
                border: 1px solid #404040;
                border-radius: 6px;
                background-color: #3a3a3a;
                color: #ffffff;
            }
            .btn {
                width: 100%;
                padding: 12px;
                background-color: #d4af37;
                color: #1a1a1a;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-weight: 600;
                font-size: 1rem;
            }
            .btn:hover {
                background-color: #b8941f;
            }
        </style>
    </head>
    <body>
        <div class="login-container">
            <h1>🔐 Login Administrativo</h1>
            <form onsubmit="fazerLogin(event)">
                <div class="form-group">
                    <label for="usuario">Usuário:</label>
                    <input type="text" id="usuario" value="seuchico" readonly>
                </div>
                <div class="form-group">
                    <label for="senha">Senha:</label>
                    <input type="password" id="senha" placeholder="Digite a senha">
                </div>
                <button type="submit" class="btn">Entrar</button>
            </form>
        </div>
        
        <script>
            function fazerLogin(event) {
                event.preventDefault();
                const senha = document.getElementById('senha').value;
                
                // Senha simples para demonstração
                if (senha === 'barbearia2024') {
                    window.location.href = '/admin';
                } else {
                    alert('Senha incorreta!');
                }
            }
        </script>
    </body>
    </html>
    """)

