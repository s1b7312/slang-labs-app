
import os
import json
import logging
from flask import Flask, request, Response

from config import app_config
from utils import is_allowed_extension
from tfidf import TfidfVectorizer

logging.basicConfig(level=logging.DEBUG, filename='logs.log', format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.update(app_config)

tfidf_obj = TfidfVectorizer()


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        logger.error('No files detected. Use "files" key')
        return Response('No files detected!! Use "files" key', status=400)

    files = request.files.getlist('files')
    valid = 0
    for f in files:
        # print(f.filename)
        if not is_allowed_extension(f.filename):
            continue
        try:
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
            valid += 1
        except Exception as e:
            logger.error('Could not save file %s', f)
    logging.info('Uploaded %d files', valid)

    try:
        tfidf_obj.from_dir(app.config['UPLOAD_FOLDER'])
        return Response(f'{valid} files uploaded and vectorizer trained..', status=200)
    except Exception as e:
        return Response(f'Error occurred: {e}', status=500)


@app.route('/query', methods=['POST'])
def query():
    if 'query' not in request.json:
        logger.error('Query not detected. Use "query" key')
        return Response('Query not detected!! Use "query" key', status=400)

    try:
        query = request.json['query']
        matches = tfidf_obj.query(query)
        # return Response(matches, status=200, content_type='application/json')
        return json.dumps(matches)
    except Exception as e:
        logging.error('Error occurred', e)
        return Response(f'Error occurred: {e}', status=500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
