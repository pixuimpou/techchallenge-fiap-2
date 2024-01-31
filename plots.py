import matplotlib.pyplot as plt
import statsmodels.api as sm


def plot_seasonal_decompose(timeseries, mode="show"):
    decomposition = sm.tsa.seasonal_decompose(timeseries, model="additive")
    decomposition.plot()
    plt.xticks(rotation=45)
    if mode == "show":
        plt.show()
    else:
        plt.gcf()


def plot_arima_forecast(
    real_values,
    forecast_values,
    confidence_intervals,
    title,
    mode="show",
):
    ax = real_values.plot(label="Valor real")
    forecast_values.plot(ax=ax, label="Previsão", alpha=0.7, figsize=(14, 7))
    ax.fill_between(
        confidence_intervals.index,
        confidence_intervals.iloc[:, 0],
        confidence_intervals.iloc[:, 1],
        color="k",
        alpha=0.2,
    )
    ax.set_xlabel("Data")
    ax.set_ylabel("Valor Fechamento")
    plt.title(title)
    plt.legend()
    if mode == "show":
        plt.show()
    else:
        plt.gcf()


def plot_svm(timestamps, y_test, svm_predictions, mode="show"):
    plt.figure(figsize=(25, 6))
    plt.plot(timestamps, y_test, color="red", linewidth=2.0, alpha=0.6)
    plt.plot(timestamps, svm_predictions, color="blue", linewidth=0.8)
    plt.legend(["Valor Real", "Previsão"])
    plt.xlabel("Data")
    plt.title("Resultado SVM")
    if mode == "show":
        plt.show()
    else:
        plt.gcf()
