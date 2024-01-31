import streamlit as st
import altair as alt
import pandas as pd
import joblib
from utils import Config, create_driver_path
from constants import constants
from plots import plot_seasonal_decompose, plot_svm
from model_utils import split_x_y, aggregate_data_in_timesteps


config = Config()

st.title("Tech Challenge - Fase 2")
st.divider()
st.markdown("# O Desafio")
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
st.markdown("### Dados tratados:")
st.markdown("Após os tratamentos, ficamos com a seguinte série temporal:")
df_timeseries = pd.read_csv(
    create_driver_path(file_id=constants.TIMESERIES_FILE_ID.value)
)
df_timeseries["data"] = pd.to_datetime(df_timeseries["data"])
df_timeseries["data"] = pd.date_range(
    df_timeseries["data"].min(), df_timeseries["data"].max()
)
df_timeseries = df_timeseries.set_index("data", drop=True)

st.write(df_timeseries.head(20))

st.markdown("## Análise da série temporal")
st.line_chart(df_timeseries)
st.write(
    """
    O gráfico acima mostra os valores de fechamento da bolsa ao decorrer do tempo.
    Por ele já é possível ver que os dados possuem uma tendência positiva
    """
)
st.markdown("### Visualização da tendência e sazonalidade dos dados")
st.markdown(
    """Para melhor visualização e entendimento dos dados,
    nessa etapa serão analisados os dados a partir de 2023
    """
)
st.set_option("deprecation.showPyplotGlobalUse", False)
timeseries = df_timeseries["ultimo"]
st.pyplot(plot_seasonal_decompose(timeseries=timeseries["2023":], mode="gcf"))
st.write(
    """A partir do gráfico no centro,
    é possivel notar a sazonalidade nos dados
    e, mais uma vez, a tendencia de subida"""
)
st.divider()
st.markdown("## Modelo Final")
st.write(
    """
    Após testes com modelos de previsão de séries temporais,
    o modelo escolhido foi o SVM,
    por conta da sua performance superior para os dados"""
)

train_size = int(len(timeseries) * constants.TEST_PERCENTAGE.value)
test = timeseries[train_size:]
test_data = test.values
timesteps = constants.TIMESTEPS.value
test_data_timesteps = aggregate_data_in_timesteps(test_data, timesteps)
x_test, y_test = split_x_y(test_data_timesteps, timesteps)

model = joblib.load("modelo.pkl")

predictions = model.predict(x_test).reshape(-1, 1)
test_timestamps = timeseries[train_size:].index[timesteps - 1 :]

df_real = pd.DataFrame(
    y_test, index=test_timestamps, columns=["valor_real"]
).reset_index()
df_pred = pd.DataFrame(
    predictions, index=test_timestamps, columns=["previsão"]
).reset_index()

chart = alt.Chart(df_real).mark_line().encode(
    x="data",
    y="valor_real",
    color=alt.value("blue"),  # Cor da linha para Coluna A
) + alt.Chart(df_pred).mark_line().encode(
    x="data",
    y="previsão",
    color=alt.value("red"),  # Cor da linha para Coluna B
)

st.altair_chart(chart, use_container_width=True)


st.pyplot(
    plot_svm(test_timestamps[-100:], y_test[-100:], predictions[-100:], mode="gcf")
)

st.write("Pela proximidade nas linhas n")
