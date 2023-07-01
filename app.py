from flask import *
import pandas as pd
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key = 'This is your secret key to utilize session in Flask'

@app.route('/',methods=['GET','POST'])
def uploadFile():
    if request.method == 'POST':
        f = request.files.get('file')
        data_filename = secure_filename(f.filename)
        f.save(data_filename)
        session['uploaded_data_file_path'] = data_filename
        return render_template("home_page_before.html")
    return render_template("home_page_after.html")

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

@app.route('/show_head')
def showHead():
    # Uploaded File Path
    data_file_path = session.get('uploaded_data_file_path', None)
    # read csv
    uploaded_df = pd.read_csv(data_file_path,
                              encoding='unicode_escape').head()
    # Converting to html Table
    uploaded_df_html = uploaded_df.to_html()
    return render_template('show_csv_head.html',
                           data_var=uploaded_df_html)

if __name__ == '__main__':
    app.run(debug=True)