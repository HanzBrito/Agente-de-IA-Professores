# Agente de IA para Professores (AgenteIaProfessor Crew)

Sistema multiagente de IA construído com o framework [crewAI](https://crewai.com), voltado ao apoio de professores. Os agentes colaboram em tarefas definidas por configuração e rodam **100% localmente** com um LLM servido pelo [Ollama](https://ollama.com) (modelo `llama3.2`), sem necessidade de chaves de API externas.

> **[ajuste]** Descreva aqui, em 2–3 frases, o que seus agentes fazem na prática (ex.: planejar aulas, criar exercícios, corrigir atividades).

## Sumário

- [Visão geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração do LLM local (Ollama)](#configuração-do-llm-local-ollama)
- [Personalização](#personalização)
- [Execução](#execução)
- [Solução de problemas](#solução-de-problemas)
- [Suporte](#suporte)

## Visão geral

O projeto usa o conceito de **Crew** do crewAI: um conjunto de agentes, cada um com papel (`role`), objetivo (`goal`) e histórico (`backstory`), que executam tarefas em sequência e colaboram para entregar um resultado final.

Vantagens da abordagem com LLM local:

- **Privacidade:** nenhum dado sai da sua máquina.
- **Custo zero** por requisição.
- **Funciona offline** após o download do modelo.
- **Modelo intercambiável:** basta alterar uma variável no `.env`.

## Arquitetura

```
 .env ──► main.py ──► crew.py ──► Agentes (agents.yaml)
 (config)  (entrada)  (orquestra)   │
                                    ▼
                              Tarefas (tasks.yaml)
                                    │
                                    ▼
                        Ollama (localhost:11434)
                            modelo llama3.2
                                    │
                                    ▼
                          Resultado (ex.: report.md)
```

1. `main.py` recebe os inputs e dispara a crew.
2. `crew.py` monta agentes e tarefas a partir dos arquivos YAML.
3. Cada agente consulta o LLM local via Ollama.
4. O resultado final é gravado em arquivo conforme definido em `tasks.yaml`.

## Estrutura do projeto

```
.
├── .env                      # Variáveis de ambiente (NÃO versionar)
├── .env.example              # Modelo de configuração (versionar)
├── pyproject.toml            # Dependências (gerenciadas com uv)
├── README.md
└── src/agente_ia_professor/
    ├── config/
    │   ├── agents.yaml       # Definição dos agentes
    │   └── tasks.yaml        # Definição das tarefas
    ├── tools/                # Ferramentas customizadas (opcional)
    ├── crew.py               # Lógica da crew
    └── main.py               # Ponto de entrada
```

## Pré-requisitos

- Python `>=3.10` e `<3.14`
- [uv](https://docs.astral.sh/uv/) para gerenciamento de dependências
- [Ollama](https://ollama.com/download) instalado
- Memória RAM suficiente para o modelo (o `llama3.2` de 3B roda bem em máquinas modestas)

## Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/HanzBrito/Agente-de-IA-Professores.git
cd Agente-de-IA-Professores

# 2. Instale o uv (se ainda não tiver)
pip install uv

# 3. Instale as dependências
crewai install
```

## Configuração do LLM local (Ollama)

### 1. Baixe o modelo

```bash
ollama pull llama3.2
ollama list          # confirme que llama3.2 aparece na lista
```

O servidor do Ollama deve estar ativo (`ollama serve`, ou em segundo plano após a instalação) e responde por padrão em `http://localhost:11434`.

### 2. Configure o arquivo `.env`

Copie o modelo e edite:

```bash
cp .env.example .env
```

Exemplo de conteúdo **[ajuste: use os nomes de variáveis que o seu `crew.py` lê]**:

```env
# Modelo local servido pelo Ollama (prefixo "ollama/" exigido pelo crewAI/LiteLLM)
MODEL=ollama/llama3.2

# Endereço do servidor Ollama
API_BASE=http://localhost:11434
```

| Variável   | Descrição                                   | Valor padrão              |
|------------|---------------------------------------------|---------------------------|
| `MODEL`    | Modelo local utilizado pelos agentes        | `ollama/llama3.2`         |
| `API_BASE` | URL do servidor Ollama                      | `http://localhost:11434`  |

> **Importante:** como o LLM é local, **não é necessário** definir `OPENAI_API_KEY`. O trecho do template original que pede essa chave não se aplica a este projeto.
> Nunca faça commit do `.env`. Garanta que ele esteja no `.gitignore`.

## Personalização

| Arquivo                                      | O que alterar                                      |
|----------------------------------------------|----------------------------------------------------|
| `src/agente_ia_professor/config/agents.yaml` | Papéis, objetivos e histórico dos agentes          |
| `src/agente_ia_professor/config/tasks.yaml`  | Descrição das tarefas e saídas esperadas           |
| `src/agente_ia_professor/crew.py`            | Lógica da crew, ferramentas e configuração do LLM  |
| `src/agente_ia_professor/main.py`            | Inputs customizados (ex.: disciplina, série, tema) |

## Execução

Com o Ollama ativo e o `.env` configurado, execute na raiz do projeto:

```bash
crewai run
```

O comando inicializa a crew, monta os agentes e executa as tarefas definidas na configuração. O resultado é salvo no arquivo indicado em `tasks.yaml` (no template original, `report.md`). **[ajuste: informe o arquivo de saída do seu projeto]**

## Solução de problemas

| Problema                                  | Solução                                                              |
|-------------------------------------------|----------------------------------------------------------------------|
| `Connection refused` na porta 11434       | Inicie o servidor: `ollama serve`                                    |
| `model "llama3.2" not found`              | Execute `ollama pull llama3.2`                                       |
| Erro pedindo `OPENAI_API_KEY`             | Verifique se `MODEL` e `API_BASE` estão corretos e se o LLM é passado aos agentes em `crew.py` |
| Respostas lentas                          | Normal em CPU; feche outros programas ou use GPU                     |

## Suporte

Para dúvidas sobre o crewAI:

- [Documentação](https://docs.crewai.com)
- [Repositório do crewAI](https://github.com/crewAIInc/crewAI)
- [Comunidade no Discord](https://discord.com/invite/X4JWnZnxPb)

Para dúvidas sobre este projeto, abra uma *issue* neste repositório.
