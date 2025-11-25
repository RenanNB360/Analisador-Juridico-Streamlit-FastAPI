# JusCash Case AI - Verificador de Processos Judiciais

Este projeto é uma solução automatizada para análise de elegibilidade de processos judiciais. Utilizando **Inteligência Artificial (LLM)**, o sistema lê dados estruturados de processos, verifica conformidade com as Políticas Internas (POL-1 a POL-8) e fornece um veredito estruturado (Aprovado, Reprovado ou Incompleto) com justificativa jurídica.

---

## Links Públicos da Aplicação

> A aplicação está rodando em ambiente de produção no **Render**, dividida em dois microsserviços (Frontend e Backend).

> **⚠️ IMPORTANTE - COLD START (Plano Gratuito):**
> Como a hospedagem é gratuita, o servidor da API "dorme" após 15 minutos de inatividade.
> **Passo recomendado para teste:**
> 1. Clique no link da **API (Docs)** primeiro e aguarde carregar (pode levar de 40 a 60 segundos).
> 2. Assim que a API carregar, abra o link da **Interface Visual**.
> 3. Se abrir a Interface direto, pode ocorrer um erro de conexão inicial. Basta aguardar e recarregar a página.

- ** Interface Visual (UI):** https://juscash-frontend.onrender.com
- ** Documentação da API (Swagger):** https://juscash-backend.onrender.com/docs
- ** Health Check:** https://juscash-backend.onrender.com/health

---

## Como Rodar Localmente (Docker)

O projeto foi dividido em microsserviços. Você precisará de **dois terminais** abertos para rodar o sistema completo.

### 1. Pré-requisitos

- Docker instalado
- Arquivo `.env` na raiz do projeto com as chaves necessárias (OpenAI/OpenRouter, LangSmith)

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

### 2. Executando o Backend (API)

No primeiro terminal, construa e rode a API:

```bash
# Constrói a imagem do Backend usando a raiz como contexto
docker build -f backend/Dockerfile -t juscash-backend .

# Roda o container na porta 8000 (lendo o arquivo .env)
docker run -p 8000:8000 --env-file .env juscash-backend
```
**Aguarde aparecer "Application startup complete".**

### 3. Executando o Frontend (UI)

No segundo terminal, construa e rode o Streamlit:

```bash
# Constrói a imagem do Frontend
docker build -f frontend/Dockerfile -t juscash-frontend .

# Roda o container na porta 8501
# Nota: --network="host" é recomendado para Linux para facilitar a comunicação com localhost:8000
# Se estiver no Windows/Mac, use -e API_URL="http://host.docker.internal:8000"

docker run -p 8501:8501 --network="host" -e API_URL="http://localhost:8000" juscash-frontend
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