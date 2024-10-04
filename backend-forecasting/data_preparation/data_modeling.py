from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX

class DataTrain:
    def __init__(self, trend_data_train, seasonal_data_train) -> None:
        self.trend_data_train = trend_data_train
        self.seasonal_data_train = seasonal_data_train


    def trend_data_modeling(self, p, d, q):
        model = ARIMA(self.trend_data_train, order=(p, d, q))
        model_fit = model.fit()
        return model_fit

    def seasonal_data_modeling(self, p, d, q, P, D, Q, m):
        if self.seasonal_data_train != None:
          model = SARIMAX(self.seasonal_data_train, order=(p, d, q), seasonal_order=(P, D, Q, m))
          model_fit = model.fit()
          return model_fit
        else:
          return "error need seasonal data"
