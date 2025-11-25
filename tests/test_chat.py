from datetime import datetime
from unittest.mock import patch

import pytest

from backend.schemas.schemas_api import Documento, Processo
from backend.schemas.schemas_service import AnaliseJuridica
from backend.service.chat import analisar_processo


@pytest.fixture
def processo_exemplo():
    return Processo(
        numeroProcesso="0001234-56.2023.4.05.8100",
        classe="Cumprimento de Sentença",
        orgaoJulgador="Vara Federal",
        ultimaDistribuicao=datetime.now(),
        assunto="Rural",
        segredoJustica=False,
        justicaGratuita=True,
        siglaTribunal="TRF5",
        esfera="Federal",
        valorCondenacao=10000.00,
        documentos=[
            Documento(
                id="1",
                dataHoraJuntada=datetime.now(),
                nome="Petição",
                texto="Conteúdo teste"
            )
        ],
        movimentos=[]
    )


@patch('backend.service.chat.logger')
@patch('backend.service.chat.chain')
def test_analisar_processo_ok(mock_chain, mock_logger, processo_exemplo):
    result_fake_llm = AnaliseJuridica(
        decision='approved',
        rationale='O processo cumpre os requisitos.',
        citacoes=['Lei 123']
    )

    mock_chain.invoke.return_value = result_fake_llm
    result = analisar_processo(processo_exemplo)

    assert result == result_fake_llm
    assert result.decision == 'approved'

    mock_chain.invoke.assert_called_once()
    assert mock_logger.info.call_count >= 2


@patch('backend.service.chat.logger')
@patch('backend.service.chat.chain')
def test_analisar_processo_except(mock_chain, mock_logger, processo_exemplo):
    message_erro = 'Erro de conexão com OpenRouter'
    mock_chain.invoke.side_effect = Exception(message_erro)

    with pytest.raises(Exception) as exec_info:
        analisar_processo(processo_exemplo)

    assert message_erro in str(exec_info.value)

    mock_logger.error.assert_called_once()
    args, _ = mock_logger.error.call_args
    log_message = args[0]
    assert processo_exemplo.numeroProcesso in log_message
