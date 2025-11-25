from datetime import datetime
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from fastapi import status
from backend.app import app
from backend.schemas.schemas_api import Processo, Documento

client = TestClient(app)

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
    ).model_dump(mode="json")


def test_health_check():
    response = client.get('/health')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'ok'}


@patch("backend.app.analisar_processo")
@patch("backend.app.logger")
def test_analyze_ok(mock_logger, mock_analisar, processo_exemplo):
    result_fake = {
        'decision': 'approved', 
        'rationale': 'ok', 
        'citacoes': []
    }
    mock_analisar.return_value = result_fake
    response = client.post('/analyze', json=processo_exemplo)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == result_fake

    mock_logger.info.assert_called_once()
    mock_analisar.assert_called_once()


@patch("backend.app.analisar_processo")
@patch("backend.app.logger")
def test_analyze_error(mock_logger, mock_analisar, processo_exemplo):
    mock_analisar.side_effect = Exception('Falhou!')
    response = client.post('/analyze', json=processo_exemplo)

    assert response.status_code == 500
    assert 'Erro interno' in response.json()['detail']

    mock_logger.error.assert_called_once()