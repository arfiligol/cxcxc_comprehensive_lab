from google.auth.credentials import AnonymousCredentials
from google.cloud import storage
from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

# 指定 gcs-emulator host
os.environ["STORAGE_EMULATOR_HOST"] = "http://gcs-emulator.cxcxc.pri:4443"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@mysqldb.cxcxc.pri/app1-web'
db = SQLAlchemy(app)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255), index=True)
    file_url = db.Column(db.String(255))

def store_file_in_gcs(file):
    client = storage.Client(credentials=AnonymousCredentials(), project="test")
    bucket = client.get_bucket('app1-web-bucket')

    blob = bucket.blob(file.filename)
    blob.upload_from_string(
        file.read(),
        content_type=file.content_type
    )

    url = blob.public_url

    return url

def store_in_db(file_name, url):
    file = File(file_name=file_name, file_url=url)
    db.session.add(file)
    db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_name = file.filename
            print(file_name)
            url = store_file_in_gcs(file)
            store_in_db(file_name, url)

            return redirect(url_for('upload_file', file_name=file_name))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=True)
