import pandas as pd

class Data:
    def __init__(self, data_url) -> None:
        self.data_url = data_url

    def clean_data(self):
        df = self.data_url
        df.rename(columns = {"ï»¿Date": "Date"}, inplace=True)
        df.rename(columns = {" Quantity ": "Quantity"}, inplace=True)
        selected_columns = ['Date','Quantity']
        df_selected = df[selected_columns]

        return df_selected

    def change_dataframe_index(self):
        df = self.clean_data()
        df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
        df.set_index('Date', inplace=True)
        return df

    def group_data_by_date(self):
        df = self.change_dataframe_index()
        grouped_df = df.groupby(df.index).sum()
        grouped_df.sort_index(ascending=True, inplace=True)
        return grouped_df


    def add_zero_data(self):
        clean_data = self.group_data_by_date()
        clean_data_start_index = clean_data.index[0]
        clean_data_last_index = clean_data.index[-1]
        date_range = pd.date_range(start=clean_data_start_index, end=clean_data_last_index, freq='D')
        null_value = pd.DataFrame(0, index=date_range, columns=['Quantity'])

        truncated_data = null_value.add(clean_data, fill_value=0)
        truncated_data['Quantity'] = truncated_data['Quantity'].round().astype(int)
        return truncated_data


    def create_daily_data_train(self):
        clean_data = self.add_zero_data()
        length = len(clean_data)
        df_80 = clean_data.head(int(length * 0.8))

        return df_80
    
    def create_daily_data_train_actual(self):
        clean_data = self.add_zero_data()

        return clean_data

    def create_daily_data_test(self):
        clean_data = self.add_zero_data()
        length = len(clean_data)
        df_20 = clean_data.tail(int(length * 0.2))

        return df_20

    def create_weekly_data_train(self):
        weekly_data = self.group_data_by_date().resample('W').sum()
        weekly_data.sort_index(ascending=True, inplace=True)
        length = len(weekly_data)
        df_80 = weekly_data.head(int(length * 0.8))
        return df_80

    def create_weekly_data_test(self):
        weekly_data = self.group_data_by_date().resample('W').sum()
        weekly_data.sort_index(ascending=True, inplace=True)
        length = len(weekly_data)
        df_20 = weekly_data.tail(int(length * 0.2))
        return df_20


    def create_monthly_data_train(self):
        monthly_data = self.group_data_by_date().resample('M').sum()
        monthly_data.sort_index(ascending=True, inplace=True)
        length = len(monthly_data)
        df_80 = monthly_data.head(int(length * 0.8) + 1)
        return df_80

    def create_monthly_data_test(self):
        monthly_data = self.group_data_by_date().resample('M').sum()
        monthly_data.sort_index(ascending=True, inplace=True)
        length = len(monthly_data)
        df_20 = monthly_data.tail(int(length * 0.2))
        return df_20