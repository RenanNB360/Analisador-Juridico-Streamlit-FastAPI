# JusCash Case AI - Verificador de Processos Judiciais

Este projeto é uma solução automatizada para análise de elegibilidade de processos judiciais. Utilizando **Inteligência Artificial (LLM)**, o sistema lê dados estruturados de processos, verifica conformidade com as Políticas Internas (POL-1 a POL-8) e fornece um veredito estruturado (Aprovado, Reprovado ou Incompleto) com justificativa jurídica.

---

## Links Públicos da Aplicação

> **Nota:** A aplicação está rodando em container Docker em ambiente de produção (Render/Railway).

- ** Interface Visual (UI):** [COLE_O_LINK_DO_SEU_STREAMLIT_AQUI]
- ** Documentação da API (Swagger):** [COLE_O_LINK_DA_SUA_API_AQUI]/docs
- ** Health Check:** [COLE_O_LINK_DA_SUA_API_AQUI]/health

---

## Como Rodar Localmente (Docker)

O projeto foi containerizado para garantir execução idêntica em qualquer ambiente. Siga os passos abaixo:

### 1. Pré-requisitos

- Docker instalado
- Arquivo `.env` na raiz do projeto com as chaves necessárias (OpenAI/OpenRouter, LangSmith)

### 2. Configuração do .env

Por razões de segurança, as chaves de API não foram incluídas no repositório público.

1. Localize o arquivo **`.env`** enviado em anexo na entrega deste case (e-mail ou plataforma).
2. Salve o arquivo na **raiz do projeto** (mesmo local onde está o `Dockerfile`).
3. O conteúdo esperado do arquivo é semelhante a este (apenas para conferência):

```bash
# LLM Provider
OPENROUTER_API_TOKEN="chave-api"
OPENROUTER_BASE_URL="http-OpenRouter"

# Observabilidade (Opcional mas recomendado)
LANGCHAIN_TRACING_V2=true
LANGSMITH_ENDPOINT="http-langsmith"
LANGCHAIN_API_KEY="chave-langsmith"
LANGCHAIN_PROJECT="Case-JusCash"
```
**Atenção: Sem este arquivo na raiz, a aplicação não conseguirá se comunicar com o modelo de IA.**

### 3. Build e Execução

Execute o comando abaixo para construir a imagem única (que contém tanto o Backend quanto o Frontend):

```bash
docker build -t juscash-app .
```

Em seguida, inicie o container expondo as portas da API (8000) e da UI (8501):

```bash
docker run -p 8000:8000 -p 8501:8501 --env-file .env juscash-app
```

### 4. Acessando Localmente

- **Frontend (Streamlit):** http://localhost:8501
- **API Docs (Swagger):** http://localhost:8000/docs

---

## Endpoints da API

A API foi desenvolvida com FastAPI e segue o padrão OpenAPI.

| Método | Endpoint   | Descrição                                                                                              |
|--------|------------|--------------------------------------------------------------------------------------------------------|
| GET    | `/health`  | Retorna `{status: "ok"}` para monitoramento de uptime                                                 |
| GET    | `/docs`    | Interface interativa do Swagger UI para testar endpoints e ver schemas                                |
| POST   | `/analyze` | Recebe o JSON do processo e retorna a decisão estruturada (approved, rejected, incomplete) com rationale |

---

## Arquitetura e Tecnologias

O projeto segue uma arquitetura desacoplada e modular:

- **Linguagem:** Python 3.13
- **Backend:** FastAPI (Alta performance e validação com Pydantic)
- **Frontend:** Streamlit (Interface limpa para testes manuais e visualização de feedback)
- **IA/LLM:** LangChain + Gemma/Llama (via OpenRouter/HuggingFace) para raciocínio jurídico
- **Gerenciamento de Dependências:** uv (para builds rápidos e seguros)

---

## Observabilidade e Orquestração (LangSmith)

O fluxo da IA é totalmente orquestrado e monitorado via LangChain & LangSmith. Isso garante:

- **Rastreabilidade:** Cada decisão da IA gera um Trace com inputs, outputs e latência
- **Versionamento de Prompts:** O prompt utilizado é versionado, garantindo reprodutibilidade

![Demonstração do Trace no LangSmith](assets/demo_langsmith.gif)

*(Visualização animada do painel de Observabilidade)*

---

## 🧪 Testes e Qualidade

O projeto conta com testes automatizados para garantir a robustez das regras de negócio.

- **Testes de Integração:** Validam os endpoints da API
- **Testes Unitários:** Validam se a IA está respeitando as regras críticas (ex: Rejeitar processos trabalhistas ou valores abaixo de R$ 1.000)

Para rodar os testes (caso tenha o ambiente dev configurado):

```bash
task test
```