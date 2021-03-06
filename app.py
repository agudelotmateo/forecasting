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
    print_error = 'results' in session
    save_plots = 'plots' not in session
    session['results'], error, plots = forecast_from_csv(
        current_csv_path(), session['folder_path'] if save_plots else None)
    if save_plots:
        session['plots'] = plots
    session['iterations'] -= 1
    return render_forecasting_results(error if print_error else None)

def render_initial_forecasting_form():
    session.clear()
    return render_template('forecasting.html')

def render_forecasting_results(error):
    return render_template(
        'forecasting.html', results=session['results'], error=error,
        done=session['iterations'] == 0, plots=session['plots'])

def save_plots(plots, path_identifier='folder_path', prefix='plot'):
    folder = session[path_identifier]
    session['plots'] = []
    names = session['results'][0][1:]
    for i in range(len(plots)):
        path = util.join_paths(folder, f'{prefix}-{names[i]}.png')
        session['plots'].append(path)
        plots[i].savefig(path)

def store_iterations(value, identifier='iterations'):
    session[identifier] = value

def read_iterations():
    return read_integer_element('iterations')

def read_new_row():
    # TODO: correct row
    return [0] + [ read_integer_element(column_name)
                   for column_name in session['results'][0][1:] ]

def read_integer_element(tag_name):
    element = request.form.get(tag_name)
    if not element:
        raise ValueError(f'No {tag_name} value provided')
    if not element.isdigit():
        raise ValueError(f'The {tag_name} provided is not a valid number')
    return int(element)

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

def current_csv_path():
    return csv_path(session['iterations'])

def csv_path(index, path_identifier='folder_path', prefix='data'):
    return util.join_paths(session[path_identifier], f'{prefix}-{index}.csv')


if __name__ == '__main__':
    app.run()
