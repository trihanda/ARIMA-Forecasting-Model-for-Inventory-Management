


####################################################################################################

from data_preparation.data_cleansing import Data
from data_preparation.data_modeling import DataTrain
from sklearn.metrics import mean_absolute_percentage_error

#####################################################################################################
import pandas as pd
#####################################################################################################


def predict(path):

    # membersihkan data dari file yang telah diupload dan memecahnya menjadi train dan test data
    data = Data(path)
    daily_data_train = data.create_daily_data_train() 
    daily_data_test = data.create_daily_data_test()

    actual_forecast = data.create_daily_data_train_actual()

    # membuat object untuk ditrain dan test
    daily_training = DataTrain(daily_data_train, daily_data_train) 

    # object untuk melakukan forcast tanpa pemotongan data
    daily_actual_training = DataTrain(actual_forecast, actual_forecast) 

    x = 6
    y = 0
    z = 3

    # membuat model untuk di test
    daily_model = daily_training.trend_data_modeling(x, y, z) 

    # membuat model untuk di forecast
    daily_actual_model = daily_actual_training.trend_data_modeling(x, y, z)


    # melakukan forecast dari model sebelumnya
    forecast_actual = daily_actual_model.forecast(90) 
    forecast_test = daily_model.forecast(90)

    # melakukan test dari hasil forecast sebelumnya
    mape = mean_absolute_percentage_error(daily_data_test.iloc[0:90], forecast_test) * 100 




    # format hasil forecast untuk supaya bisa di kirim menjadi json
    forecasted_data = pd.DataFrame(forecast_actual) 

    df_history = actual_forecast.iloc[-15:]
    history_data = df_history
    history_data.reset_index(inplace=True)
    history_data["Quantity"] = history_data["Quantity"].round().astype(int)
    history_dict = history_data.to_dict('list')

    forecasted_data.reset_index(inplace=True)
    forecasted_data["predicted_mean"] = forecasted_data["predicted_mean"].round().astype(int)
    forecasted_data["index"] = forecasted_data["index"].astype(str)
    forecasted_dict = forecasted_data.to_dict('list')

    data = {
        "history": history_dict,
        "forecast": forecasted_dict,
        "last_data_historical": history_data["index"].astype(str).iloc[-1],
        "error": str(mape).split('.')[0]
    }

    return data