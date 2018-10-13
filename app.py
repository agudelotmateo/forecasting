from flask import Flask, request, render_template
from util import generate_unused_folder_path, create_folder, save_csv


app = Flask(__name__)

@app.route('/')
def render_landing_page():
    return render_template('index.html')

@app.route('/forecasting', methods=['GET', 'POST'])
def render_forecasting_page():
    if request.method == 'GET':
        # TODO
        results = forecast_from_csv()
        names = ['p1', 'p2', 'p3']
        return render_template('forecasting.html', items=names, forecast=results)

    csv = request.files['data_file']
    if not file:
        return ('No file was uploaded', 400)
    session['iterations'] = requst.form.get('iterations')
    if not iterations:
        return ('No iterations number was provided', 400)
    if not iterations.isdigit():
        return ('The iterations provided is not a valid number', 400)
    session['folder_path'] = generate_unused_folder_path()
    create_folder(session['folder_path'])
    save_csv(csv, session['folder_path'], 'data')
    

if __name__ == '__main__':
    # TODO
    # app.run()
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')
