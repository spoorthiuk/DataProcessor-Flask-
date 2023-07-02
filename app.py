from flask import *
import pandas as pd
from werkzeug.utils import secure_filename
import libraries as lib
import requests

app = Flask(__name__)

app.secret_key = 'This is your secret key to utilize session in Flask'

@app.route('/',methods=['GET','POST'])
def uploadFile():
    if request.method == 'POST':
        f = request.files.get('file')
        data_filename = secure_filename(f.filename)
        f.save(data_filename)
        session['uploaded_data_file_path'] = data_filename
        return render_template("home_page_after.html")
    return render_template("home_page_before.html")

@app.route('/show_data')
def showData():
    # Uploaded File Path
    data_file_path = session.get('uploaded_data_file_path', None)
    # read csv
    uploaded_df = pd.read_csv(data_file_path,
                              encoding='unicode_escape')
    # Converting to html Table
    uploaded_df_html = uploaded_df.to_html()
    return render_template('show_csv_data.html',
                           data_var=uploaded_df_html)

@app.route('/show_head',methods=['POST'])
def showHead():
    # Uploaded File Path
    data_file_path = session.get('uploaded_data_file_path', None)
    # read csv
    row_count = request.form['row_count']
    uploaded_df = pd.read_csv(data_file_path,
                              encoding='unicode_escape').head(int(row_count))
    # Converting to html Table
    uploaded_df_html = uploaded_df.to_html()
    return render_template('show_csv_head.html',
                           data_var=uploaded_df_html)

@app.route('/get_data_description')
def showDataDescription():
    # Uploaded File Path
    data_file_path = session.get('uploaded_data_file_path', None)
    # read csv
    File = lib.FileDefinition(data_file_path)
    uploaded_df = pd.read_csv(data_file_path,
                              encoding='unicode_escape')
    data_description = File.get_column_description(file_contents=uploaded_df)
    # Converting to html Table
    html_output = '<table>'
    for key, value in data_description.items():
        html_output += '<tr><td style="color: red;>{}:</td>'.format(key, value)
        for key2, value2 in data_description[key].items():
            html_output += '<tr><td>{}</td><td>{}</td></tr>'.format(key2, value2)
    html_output += '</table>'
    
    return render_template('show_data_description.html',
                           data_var=html_output)

@app.route('/get_column_analysis')
def showColumnAnalysis():
    # Uploaded File Path
    data_file_path = session.get('uploaded_data_file_path', None)
    # read csv
    File = lib.FileDefinition(data_file_path)
    uploaded_df = pd.read_csv(data_file_path,
                              encoding='unicode_escape')
    data_description = File.get_column_description(file_contents=uploaded_df)
    column_analysis = File.get_column_analysis(column_description=data_description)
    # Converting to html Table
    html_output = '<table>'
    for key, value in column_analysis.items():
        html_output += '<tr><td>{}:</td>'.format(key, value)
        for key2, value2 in column_analysis[key].items():
            if(key2 == 'red'):
                html_output += '<tr><td style="color: red">{}</td></tr>'.format(value2)
            if(key2 == 'green'):
                html_output += '<tr><td style="color: green">{}</td></tr>'.format(value2)
    html_output += '</table>'

    
    url = 'http://127.0.0.1:5000/assets/dataProcessor.png'
    response = requests.head(url)

    if response.status_code == 200:
        print("File exists!")
    else:
        print("File does not exist.")
    
    return render_template('show_column_analysis.html',
                           data_var=html_output)

if __name__ == '__main__':
    app.run(debug=True)