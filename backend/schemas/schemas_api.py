from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Movimento(BaseModel):
    dataHora: datetime
    descricao: str


class Documento(BaseModel):
    id: str = Field(..., description='ID único do documento', example='DOC-1-1')
    dataHoraJuntada: datetime
    nome: str = Field(..., description='Tipo do documento', example='Certidão de Trânsito em Julgado')
    texto: str = Field(
        ..., description='Conteúdo extraído via OCR', example='Certifico que a sentença transitou em julgado...'
    )


class Processo(BaseModel):
    numeroProcesso: str = Field(..., description='Número CNJ do processo', example='0001234-56.2023.4.05.8100')
    classe: str = Field(..., example='Cumprimento de Sentença contra a Fazenda Pública')
    orgaoJulgador: str = Field(..., example='19ª VARA FEDERAL - SOBRAL/CE')
    ultimaDistribuicao: datetime
    assunto: str = Field(..., example='Rural (Art. 48/51)')
    segredoJustica: bool = Field(False, description='Se o processo corre em segredo')
    justicaGratuita: bool
    siglaTribunal: str = Field(..., example='TRF5')
    esfera: str = Field(..., description='Federal, Estadual ou Trabalhista', example='Federal')
    valorCondenacao: Optional[float] = Field(None, description='Valor monetário da condenação', example=67592.00)
    documentos: List[Documento]
    movimentos: List[dict] = Field(default=[], description='Lista de movimentos processuais')
