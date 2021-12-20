
#Importation des librairies

import os   # Pour les manipulations de fichiers comme obtenir les chemins, renommez
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename 
import numpy as np
import pandas as pd
import glob

#Créer une instance et vérifier l'extension

app=Flask(__name__)

app.secret_key = "secret key" # pour crypter la session

#It will allow below 16MB contents only, you can change it
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

path = os.getcwd()

 # Importation des fichiers

UPLOAD_FOLDER = os.path.join(path, 'uploads')

# Créer un répertoire si le dossier "uploads" n'existe pas

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['csv', 'xls', 'csv', 'xlsx'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Routage et exécution de l'application

@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/fusion_excel')
def fusion_excel():
    return render_template('fusion_excel.html')


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        flash('File(s) successfully uploaded')
        return redirect('/fusion_excel')

@app.route('/fusionner_excel', methods=['POST'])
def fusionner_excel():
    all_data = pd.DataFrame()
    for f in glob.glob("C:/Users/HP/Desktop/flask/flask_first_web_afp/uploads/*.xlsx"):
        df = pd.read_excel(f)
        all_data = all_data.append(df,ignore_index=True)
        writer = pd.ExcelWriter('C:/Users/HP/Desktop/flask/flask_first_web_afp/uploads/site_fusionner.xlsx')
        all_data.to_excel(writer,'sheet1',index=False)
        writer.save()       
    return redirect('/')

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,debug=False,threaded=True)
