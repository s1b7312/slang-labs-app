
import os

BASE_PATH = os.getcwd()
UPLOAD_FOLDER = os.path.join(BASE_PATH, 'uploaded_files')
ALLOWED_EXTENSIONS = ['txt']

app_config = {
    'UPLOAD_FOLDER': UPLOAD_FOLDER,             # to store uploaded files
    'MAX_CONTENT_LENGTH': 4*1024*1024,          # max 4MB
    'ALLOWED_EXTENSIONS': ALLOWED_EXTENSIONS
}

VECTORIZER_FOLDER = os.path.join(BASE_PATH, 'vectorizer')


#################################################################
if not os.path.exists(app_config['UPLOAD_FOLDER']):
    os.mkdir(app_config['UPLOAD_FOLDER'])

if not os.path.exists(VECTORIZER_FOLDER):
    os.mkdir(VECTORIZER_FOLDER)
