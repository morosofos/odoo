# Documentação do Projeto: CRM Anormal (MVP - V1.0)

**Versão:** 1.0 (MVP)
**Data:** 25 de outubro de 2025

## 1. Objetivo do Projeto

O objetivo deste projeto é desenvolver o **CRM Anormal**, um Sistema de Gestão de Investimentos moderno, ágil e focado na experiência do usuário. Esta primeira versão (MVP) se concentra em fornecer as funcionalidades essenciais para a **rápida inserção de dados** (atividades e interações) e para o **acompanhamento claro** de projetos de investimento.

O principal requisito não-funcional é a **agilidade**, que será alcançada através de formulários com o mínimo de campos obrigatórios e componentes de "Adicionar Rápido".

## 2. Stack de Tecnologia

*   **Backend:** FastAPI (Python)
*   **Frontend:** HTMX (renderização de HTML dinâmico diretamente pelo backend)
*   **Banco de Dados:** PostgreSQL

## 3. Funcionalidades Centrais (Módulos)

### Módulos Incluídos na V1.0 (MVP)

*   **Gestão de Usuários e Supervisão:**
    *   Autenticação (Login/Logout).
    *   Controle de acesso (Usuário Padrão vs. Supervisor).
    *   Dashboard de Supervisão (Gestores podem ver atividades da equipe).
*   **Gestão de Empresas e Contatos:**
    *   CRUD (Criar, Ler, Atualizar, Deletar) de Empresas.
    *   CRUD de Contatos (vinculados a uma empresa).
*   **Gestão de Atividades (Tarefas):**
    *   *Requisito Crítico:* Formulário de "Adição Rápida" (mínimo de campos).
    *   Atribuição de tarefas a um responsável.
    *   Gestão de status (Pendente, Concluído) e prazos.
*   **Registro de Interações (Log):**
    *   *Requisito Crítico:* Formulário ágil para registrar (Log) telefonemas, e-mails, reuniões.
*   **Gestão de Projetos de Investimento:**
    *   Cadastro dos detalhes do projeto (valor, empregos, status) vinculado a uma empresa.

### Módulos Futuros (Pós-V1.0)

*   Gestão de After Care
*   Acompanhamento de Processos Governamentais
*   Integração com WhatsApp
*   Relatórios Avançados
*   Gestão Territorial / Site Selection
*   Inteligência de Mercado / Prospecção Ativa

## 4. Estrutura de Dados (Esquema PostgreSQL)

Este é o esquema "coração" do banco de dados para a V1.0.

```sql
-- Tabela 1: Usuários do sistema
CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hash_senha VARCHAR(255) NOT NULL,
    e_supervisor BOOLEAN DEFAULT false NOT NULL
);

-- Tabela 2: Empresas (O núcleo do CRM)
CREATE TABLE empresa (
    id SERIAL PRIMARY KEY,
    nome_fantasia VARCHAR(255) NOT NULL,
    razao_social VARCHAR(255),
    cnpj VARCHAR(14) UNIQUE,
    situacao VARCHAR(50) NOT NULL DEFAULT 'Prospecção',
    usuario_responsavel_id INT REFERENCES usuario(id) ON DELETE SET NULL,
    data_criacao TIMESTAMPTZ DEFAULT now(),
    data_ultima_alteracao TIMESTAMPTZ DEFAULT now()
);

-- Tabela 3: Contatos (Pessoas das empresas)
CREATE TABLE contato (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cargo VARCHAR(100),
    email VARCHAR(255),
    telefone VARCHAR(50),
    empresa_id INT NOT NULL REFERENCES empresa(id) ON DELETE CASCADE,
    observacao TEXT
);

-- Tabela 4: Atividades (Tarefas a fazer)
CREATE TABLE atividade (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    observacao TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'Pendente',
    data_prazo DATE,
    empresa_id INT NOT NULL REFERENCES empresa(id) ON DELETE CASCADE,
    usuario_responsavel_id INT NOT NULL REFERENCES usuario(id),
    data_criacao TIMESTAMPTZ DEFAULT now(),
    data_conclusao TIMESTAMPTZ
);

-- Tabela 5: Interações (Logs de contato)
CREATE TABLE interacao (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL, -- Ex: 'Email', 'Telefone', 'WhatsApp'
    resumo TEXT NOT NULL,
    empresa_id INT NOT NULL REFERENCES empresa(id) ON DELETE CASCADE,
    usuario_id INT NOT NULL REFERENCES usuario(id),
    data_interacao TIMESTAMPTZ DEFAULT now()
);

-- Tabela 6: Projetos (Detalhes do investimento)
CREATE TABLE projeto_investimento (
    id SERIAL PRIMARY KEY,
    empresa_id INT NOT NULL REFERENCES empresa(id) ON DELETE CASCADE,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'Análise',
    investimento_estimado_reais DECIMAL(20, 2),
    empregos_estimados_diretos INT,
    data_inicio_prevista DATE,
    data_operacao_prevista DATE
);
```
*(Nota: Tabelas para `After Care`, `Processos Governamentais` e `WhatsApp` serão adicionadas em versões futuras).*

## 5. Estrutura de Arquivos do Projeto (FastAPI + HTMX)

```
crm_anormal/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── empresas.py
│   │   └── atividades.py
│   │
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   │
│   └── templates/
│       ├── base.html
│       ├── index.html
│       └── partials/
│           ├── _form_add_atividade.html
│           └── _lista_atividades.html
│
├── .env
└── requirements.txt
```

## 6. Ordem de Implementação das Funcionalidades (V1.0)

1.  **Fundação e Autenticação:**
    *   Setup do projeto (FastAPI, DB, Git).
    *   Implementação do Módulo `usuario`.
2.  **Núcleo do CRM:**
    *   CRUD do Módulo `empresa`.
    *   CRUD do Módulo `contato`.
3.  **Módulos de Agilidade (Críticos):**
    *   CRUD do Módulo `atividade` (foco no "Adicionar Rápido").
    *   CRUD do Módulo `interacao` (foco no registro rápido).
4.  **Módulo de Negócio:**
    *   CRUD do Módulo `projeto_investimento`.
5.  **Funcionalidades de Supervisão:**
    *   Implementação do "Dashboard de Supervisão".
6.  **Finalização:**
    *   Testes finais e Deploy do MVP.
