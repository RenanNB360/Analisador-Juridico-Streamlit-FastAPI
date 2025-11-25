from fastapi import FastAPI, HTTPException, status

from backend.follow_up.config_log import logger
from backend.schemas.schemas_api import Processo
from backend.schemas.schemas_service import AnaliseJuridica
from backend.service.chat import analisar_processo
from backend.utils.addons import description

app = FastAPI(
    title='JusCash Case AI - Verificador de Processos',
    description=description,
    version='1.0.0',
)


@app.get('/health', status_code=status.HTTP_200_OK)
def health_check():
    return {'status': 'ok'}


@app.post(
    '/analyze',
    status_code=status.HTTP_200_OK,
    summary='Analisa a elegibilidade de um processo',
    description='Recebe os dados brutos de um '
    'processo e retorna a decisão de compra baseada nas políticas POL-1 a POL-8.',
    response_model=AnaliseJuridica,
    tags=['Análise'],
)
def analyze_endpoint(processo: Processo):
    logger.info('Recebendo requisição POST /analyze')
    try:
        result = analisar_processo(processo)
        return result
    except Exception as e:
        logger.error(f'Falha interna: {str(e)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Erro interno: {e}')
