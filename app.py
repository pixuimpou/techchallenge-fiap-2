import streamlit as st
import pandas as pd

from utils import Config, create_driver_path
from constants import constants

config = Config()

st.title("Tech Challenge - Fase 2")
st.divider()
st.markdown("# O Desafio:")
st.markdown("Prever diáriamente o fechamento da IBOVESPA")
st.markdown("## Captura dos Dados")
st.write(
    """Para atingir um modelo mais preciso,
    foi capturada toda a serie de dados presente no site 
    https://br.investing.com/indices/bovespa-historical-data
    através de uma raspagem de dados.
    O que compreende datas de 2000 até 2024
    """
)
st.markdown("### Dados brutos:")
st.write("Os dados foram extraídos do site para uma tabela com o seguinte formato:")
df_raw = pd.read_json(create_driver_path(file_id=constants.RAW_FILE_ID.value))
st.write(df_raw.head(20))
st.markdown("## Pre-tratamento")
st.write(
    """Para que os dados pudessem ser analizados pelo modelo,
    foi necessário aplicar uma etapa de pré-tratamento"""
)
st.markdown(
    """As etapas aplicadas foram:
    - Converter a coluna de data
    - Renomear e excluir colunas não utilizadas
    - Completar as datas ausentes (fins de semana e feriados não aparecem nos dados do site)
    """
)
st.markdown("Após os tratamentos, ficamos com a seguinte série temporal:")
df_timeseries = pd.read_csv(
    create_driver_path(file_id=constants.TIMESERIES_FILE_ID.value)
).set_index("data", drop=True)
st.write(df_timeseries.head(20))
