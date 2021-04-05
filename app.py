import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask import render_template, url_for, redirect, flash
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename


class Config(object):
    SECRET_KEY = 'hsahd&hjsak82836218hasjndksaj%hjdnfdskf8jnaskndsajgusa^6'

class UploadForm(FlaskForm):
    workspace_token = StringField('Upload string', validators=[DataRequired()])
    file_input = FileField('Upload file', validators=[FileRequired()])
    submit = SubmitField('Upload')

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = UploadForm()
    if form.validate_on_submit():
        ws_token = form.workspace_token.data.strip()
        f = form.file_input.data
        filename = secure_filename(f.filename)

        str_split=ws_token.split('/')
        sas=str_split[4]
        container_name=str_split[3]
        account_name=str_split[2].split('.')[0]
        account_url=str_split[0]+'//'+str_split[2]

        blob_service_client = BlobServiceClient(account_url=account_url, credential=sas)
        container_client = blob_service_client.get_container_client(container_name)
        
        container_client.upload_blob(name=filename,data=f)

        flash(f'The file has been uploaded: {filename}')
        return redirect(url_for('index'))
    return render_template('index.html', title='Upload a file', form=form)

@app.errorhandler(404)
def not_found_error(error):
        return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500