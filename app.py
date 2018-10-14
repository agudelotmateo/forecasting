from flask import Flask, request, session, render_template
from forecasting import forecast_from_csv
import pandas
import util


app = Flask(__name__)
app.config['SECRET_KEY'] = 'really nigga'

@app.route('/')
def render_home():
    return render_template('index.html')

@app.route('/forecasting', methods=['GET', 'POST'])
def forecasting_page():
    if request.method == 'GET':
        return render_initial_forecasting_form()
    else:
        if 'iterations' not in session:
            try:
                store_iterations(read_iterations())
            except ValueError as error:
                return str(error), 400
            create_temporary_folder_and_store_path()
            try:
                save_csv(read_csv())
            except FileNotFoundError as error:
                return str(error), 400
        elif session['iterations'] == 0:
            return render_initial_forecasting_form()
        else:
            try:
                append_row_to_new_csv_and_save(read_new_row())
            except ValueError as error:
                return str(error), 400
    session['results'] = forecast_from_csv(current_csv_path())
    session['iterations'] -= 1
    return render_forecasting_results()

def render_initial_forecasting_form():
    session.clear()
    return render_template('forecasting.html')

def render_forecasting_results():
    return render_template(
        'forecasting.html', results=session['results'], done=session['iterations'] == 0)

def store_iterations(value, identifier='iterations'):
    session[identifier] = int(value)

def read_iterations(tag_name='iterations'):
    iterations = request.form.get(tag_name)
    if not iterations:
        raise ValueError('No iterations number was provided')
    if not iterations.isdigit():
        raise ValueError('The iterations provided is not a valid number')
    return iterations

def create_temporary_folder_and_store_path(identifier='folder_path'):
    session[identifier] = util.generate_unused_folder_path()
    util.create_folder(session[identifier])

def save_csv(csv):
    return csv.save(current_csv_path())

def read_csv(tag_name='data_file'):
    csv = request.files[tag_name]
    if not csv:
        raise FileNotFoundError('No file was uploaded')
    return csv

def append_row_to_new_csv_and_save(new_row):
    original_csv_path = csv_path(session['iterations'] + 1)
    dataframe = pandas.read_csv(original_csv_path)
    dataframe.loc[len(dataframe)] = new_row
    new_csv_path = current_csv_path()
    dataframe.to_csv(new_csv_path, index=False)

def read_new_row():
    # TODO
    return [ 105 ] + [ 10000000 for _ in range(12) ]

def current_csv_path():
    return csv_path(session['iterations'])

def csv_path(index, path_identifier='folder_path', prefix='data'):
    return util.join_paths(session[path_identifier], f'{prefix}{index}.csv')

if __name__ == '__main__':
    # TODO
    # app.run()
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')
