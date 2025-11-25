import json
import os
from http import HTTPStatus

import requests
import streamlit as st

st.set_page_config(page_title='JusCash AI - Verificador', page_icon='⚖️', layout='wide')


API_URL = os.getenv('API_URL', 'http://localhost:8000')


if 'json_input' not in st.session_state:
    st.session_state['json_input'] = ''


def limpar_dados():
    st.session_state['json_input'] = ''


st.title('Analista de Processos - Case JusCash AI')
st.markdown(
    """
    **Instruções:** Cole o JSON do processo judicial na caixa abaixo e clique em **Analisar Processo**.
    A IA avaliará a elegibilidade com base nas políticas internas (POL-1 a POL-8).
    """
)

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader('Entrada de Dados')

    json_str = st.text_area(
        label='Json do Processo',
        height=500,
        placeholder='{\n  "numeroProcesso": "...",\n  "valorCondenacao": 1000,\n  ...\n}',
        help='Cole aqui o objeto JSON contendo os dados do processo, documentos e movimentos.',
        key='json_input',
    )

    b_col1, b_col2 = st.columns([3, 1])

    with b_col1:
        analisar_btn = st.button('Analisar Processo', type='primary', use_container_width=True)

    with b_col2:
        st.button('Limpar', on_click=limpar_dados, use_container_width=True)


with col2:
    st.subheader('Resultado')

    if analisar_btn:
        if not json_str.strip():
            st.warning('Por favor, insira um JSON antes de analisar.')
            st.stop()

        try:
            cleaned_json = (
                json_str.replace("'", '"').replace('True', 'true').replace('False', 'false').replace('None', 'null')
            )
            payload = json.loads(json_str)
        except json.JSONDecodeError as e:
            st.error(f'Formato Inválido. O texto inserido não é um JSON válido.\nErro: {e}')
            st.stop()

        with st.status('Processando análise...', expanded=True) as status:
            try:
                st.write(f'Enviando dados para {API_URL}...')
                response = requests.post(f'{API_URL}/analyze', json=payload)

                if response.status_code == HTTPStatus.OK:
                    data = response.json()
                    status.update(label='Análise Concluída!', state='complete', expanded=False)

                    decision = data.get('decision', '').lower()

                    if decision == 'approved':
                        st.success('APROVADO (APPROVED)')
                    elif decision == 'rejected':
                        st.error('REPROVADO (REJECTED)')
                    else:
                        st.warning('INCOMPLETO (INCOMPLETE)')

                    st.markdown('### Justificativa')
                    st.info(data.get('rationale', 'Sem justificativa retornada.'))

                    st.markdown('### Regras Citadas')
                    citacoes = data.get('citacoes', [])

                    if citacoes:
                        st.write(', '.join([f'`{c}`' for c in citacoes]))
                    else:
                        st.caption('Nenhuma regra específica citada.')

                    with st.expander('Ver JSON de Resposta'):
                        st.json(data)

                else:
                    status.update(label='Erro na API', state='error')
                    st.error(f'Erro {response.status_code}: {response.text}')

            except requests.exceptions.ConnectionError:
                status.update(label='Falha de Conexão', state='error')
                st.error(f'Não foi possível conectar à API em `{API_URL}`. Verifique se o backend está rodando.')

            except Exception as e:
                status.update(label='Erro Inesperado', state='error')
                st.error(f'Ocorreu um erro: {str(e)}')

    else:
        st.info('Aguardando dados para análise.')
