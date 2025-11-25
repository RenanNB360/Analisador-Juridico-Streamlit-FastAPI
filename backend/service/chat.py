import os

from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from backend.follow_up.config_log import logger
from backend.schemas.schemas_api import Processo
from backend.schemas.schemas_service import AnaliseJuridica
from backend.service.prompts.upload_prompt import load_prompt

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(base_dir, '..', '.env')

load_dotenv(dotenv_path)


openrouter_api = os.getenv('OPENROUTER_API_TOKEN')

model_llm = 'mistralai/mistral-7b-instruct:free'

llm = ChatOpenAI(
    model=model_llm,
    base_url=os.getenv('OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1'),
    api_key=openrouter_api,
    temperature=0,
)

parser = PydanticOutputParser(pydantic_object=AnaliseJuridica)


prompt_template = load_prompt('prompt_analise_v1')

prompt = PromptTemplate(
    template=prompt_template,
    input_variables=['processo_json'],
    partial_variables={'format_instructions': parser.get_format_instructions()},
)

chain = prompt | llm | parser


def analisar_processo(dados_input: Processo):
    try:
        logger.info(f'Iniciando análise para processo: {dados_input.numeroProcesso}')
        json_to_llm = dados_input.model_dump_json(indent=2)
        result = chain.invoke({'processo_json': json_to_llm})
        logger.info(f'Análise concluída. Decisão: {result.decision}')
        return result
    except Exception as e:
        logger.error(f'Erro ao analisar processo {dados_input.numeroProcesso}: {e}')
        raise e