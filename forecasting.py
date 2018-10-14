from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.arima_model import ARMA
from statsmodels.tsa.ar_model import AR
from pandas import read_csv

def forecast_from_csv(csv_filename):
    column_names, columns = all_but_first_columns_and_names_from_csv(csv_filename)
    results = forecast(columns)
    return format_forecasting_results(column_names, results)

def all_but_first_columns_and_names_from_csv(csv_filename):
    dataframe = read_csv(csv_filename)
    column_names = list(dataframe)[1:]
    columns = [ dataframe[column_name].apply(parse_integer_with_possible_trailing_star)
                for column_name in column_names ]    
    return column_names, columns    

def forecast(columns):
    return { method_name: list(map(max_two_decimals_if_number, map(method, columns)))
                    for method_name, method in forecasting_methods.items() }

def format_forecasting_results(column_names, results):
    matrix = []
    matrix.append([ 'Método' ] + column_names)
    for method_name, results in results.items():
        row = [ method_name ]
        for result in results:
            row.append(result)
        matrix.append(row)
    return matrix

def parse_integer_with_possible_trailing_star(string):
    clear_string = string[:-1] if string[-1] == '*' else string
    return int(clear_string)

def max_two_decimals_if_number(result):
    try:
        return f'{result:.2f}'
    except:
        return result

def autoregression(column):
    length = len(column)
    model = AR(column)
    try:
        forecast = list(model.fit().predict(length, length))[0]
    except:
        forecast = '-'
    return forecast    

def moving_average(column):
    length = len(column)
    model = ARMA(column, order=(0, 1))
    try:
        forecast = list(model.fit(disp=False).predict(length, length))[0]
    except:
        forecast = '-'
    return forecast

def autoregressive_moving_average(column):
    length = len(column)
    model = ARMA(column, order=(2, 1))
    try:
        forecast = list(model.fit(disp=False).predict(length, length))[0]
    except:
        forecast = '-'
    return forecast

def autoregressive_integrated_moving_average(column):
    length = len(column)
    model = ARIMA(column, order=(1, 1, 1))
    try:
        forecast = list(model.fit(disp=False).predict(length, length, typ='levels'))[0]
    except:
        forecast = '-'
    return forecast

def seasonal_autoregressive_integrated_moving_average(column):
    length = len(column)
    model = SARIMAX(
        column, order=(1, 1, 1), seasonal_order=(1, 1, 1, 1), enforce_invertibility=False)
    try:
        forecast = list(model.fit(disp=False).predict(length, length))[0]
    except:
        forecast = '-'
    return forecast

def simple_exponential_smoothing(column):
    length = len(column)
    model = SimpleExpSmoothing(column)
    try:
        forecast = list(model.fit().predict(length, length))[0]
    except:
        forecast = '-'
    return forecast

def holt_winter_exponential_smoothing(column):    
    length = len(column)
    model = ExponentialSmoothing(column)
    try:
        forecast = list(model.fit().predict(length, length))[0]
    except:
        forecast = '-'
    return forecast

forecasting_methods = {
    'AR': autoregression,
    'MA': moving_average,
    'ARMA': autoregressive_moving_average,
    'ARIMA': autoregressive_integrated_moving_average,
    'SARIMA': seasonal_autoregressive_integrated_moving_average,
    'SES': simple_exponential_smoothing,
    'HWES': holt_winter_exponential_smoothing
}
