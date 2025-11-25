from typing import List, Literal

from pydantic import BaseModel, Field


class AnaliseJuridica(BaseModel):
    decision: Literal['approved', 'rejected', 'incomplete'] = Field(
        description='Decisão final: approved, rejected ou imcomplete.'
    )
    rationale: str = Field(description='Justificativa clara baseada nas regras (ex: Valor abaixo de 1000).')
    citacoes: List[str] = Field(description='Lista das regras aplicadas (ex: ["POL-1","POL-3"])')
