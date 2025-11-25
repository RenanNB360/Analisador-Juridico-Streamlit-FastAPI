description = """
API de análise automática de processos judiciais usando IA.

## Funcionalidades
* **Análise de Elegibilidade**: Verifica se o processo cumpre as políticas (POL-1 a POL-8).
* **Decisão Estruturada**: Retorna JSON com veredito e justificativa.

## Regras de Negócio
O sistema utiliza um LLM para validar:
* Trânsito em julgado
* Valores de condenação
* Esfera judicial (Trabalhista = Reprovado)
"""
