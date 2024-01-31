import streamlit as st
import pandas as pd

from utils import Config

config = Config()

st.title("Tech Challenge - Fase 2")
st.markdown("## O Desafio:")
st.markdown("Prever diáriamente o fechamento da IBOVESPA")
st.divider()
st.markdown("## Captura dos Dados")
st.write(
    """Para atingir um modelo mais preciso,
    foi capturada toda a serie de dados presente no site https://br.investing.com/indices/bovespa-historical-data
    através de uma raspagem de dados.
    O que compreende datas de 2000 até 2024
    """
)
st.markdown("### Dados brutos:")
st.write("Os dados foram extraídos do site para uma tabela com o seguinte formato:")
st.write(pd.read_json(config.raw_filepath))
