from flask import Flask, render_template, request
from pragman.misc.utils import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/source', methods=['GET', 'POST'])
def source():
    if request.method == 'POST':
        form_data = request.form
        process_source_form(form_data)
        return render_template('source.html', success=True)
    return render_template('source.html')

@app.route('/analyzer', methods=['GET', 'POST'])
def analyzer():
    if request.method == 'POST':
        form_data = request.form
        process_analyzer_form(form_data)
        return render_template('analyzer.html', success=True)
    return render_template('analyzer.html')

@app.route('/sink', methods=['GET', 'POST'])
def sink():
    if request.method == 'POST':
        form_data = request.form
        process_sink_form(form_data)
        return render_template('sink.html', success=True)
    return render_template('sink.html')

@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        form_data = request.form
        process_config_form(form_data)
        return render_template('config.html', success=True)
    return render_template('config.html')

@app.route('/logs')
def logs():
    # Retrieve logs data and pass it to template
    logs_data = get_logs_data()
    return render_template('logs.html', logs=logs_data)

if __name__ == '__main__':
    app.run(debug=True)

