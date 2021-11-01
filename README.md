### Description
An application to train a tfidf vectorizer on the uploaded files

### Usage
#### Start the APIs
    cd slang_labs_app
    python app.py

#### Upload files
Runner scripts:

    cd runner_scripts
    python upload.py <path/to/dir>
This script will upload the text files in the directory and train a tfidf vectorizer.

    python query.py
This script will ask for a query, then return the most similar files