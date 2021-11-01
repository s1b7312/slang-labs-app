
import os
import math

from typing import List, Dict

from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity

# from config import VECTORIZER_FOLDER, UPLOAD_FOLDER
from .tfidf_utils import remove_punctuations, get_word_counts


class TfidfVectorizer:

    def __init__(self):
        pass

    def preprocess(self, s: str) -> List[str]:
        """
        Preprocess the string, split and return
        :param s:
        :return:
        """
        s = s.lower()
        s = remove_punctuations(s)
        # do lemmatization, other processing

        return s.split()

    def get_idf_scores(self, data: List[List[str]], vocab: Dict[str, int]) -> Dict[str, float]:
        """
        Calculate idf for all words
        :param data:
        :param vocab:
        :return:
        """

        idf = {}
        for w, i in vocab.items():
            count = 0
            for d in data:
                if w in d:
                    count += 1
            idf[w] = math.log((self.num_docs + 1) / (count + 1)) + 1

        return idf

    def fit(self, data: List[List[str]]):
        """
        Train a tfidf vectorizer on given data
        :param data: tokenized documents
        :return:
        """

        words = set()           # store all unique words
        for doc in data:
            words.update(doc)

        self.vocab = {w: i for i, w in enumerate(sorted(list(words)))}

        # calculate idf scores
        self.idf = self.get_idf_scores(data, self.vocab)
        self.tfidf = self.transform(data)

    def transform(self, data):
        """
        Get tfidf vectors for the given documents
        :param data:
        :param word_counts:
        :return:
        """

        word_counts = []
        for doc in data:    # get word counts for each document
            doc_word_counts = get_word_counts(doc)
            word_counts.append(doc_word_counts)

        # to store tfidf scores
        tfidf = csr_matrix((len(data), len(self.vocab)))

        for i in range(len(data)):
            for word, count in word_counts[i].items():

                if word in list(self.vocab.keys()):
                    tfidf_value = count / len(data[i])
                    tfidf[i, self.vocab[word]] = tfidf_value * self.idf[word]

        return tfidf

    def from_dir(self, dir: str):
        """
        Read files from a directory and run tfidf indexing
        :param dir:
        :return:
        """

        files = os.listdir(dir)
        self.num_docs = len(files)

        doc_texts = []          # text from all documents
        doc_name_list = []      # list of the file names

        for file in files:
            with open(os.path.join(dir, file)) as f:
                text = f.read()
            text = self.preprocess(text)
            doc_texts.append(text)
            doc_name_list.append(file)

        self.fit(doc_texts)
        self.doc_name_list = doc_name_list

        # save the required files
        # return

    def query(self, doc: str, k=1):
        """
        Query on the documents
        :param doc:
        :param k: return top-k matches
        :return:
        """

        if not hasattr(self, 'tfidf'):
            raise Exception('Vectorizer not trained!!')

        doc = self.preprocess(doc)
        doc_tfidf = self.transform([doc])

        sim = cosine_similarity(doc_tfidf, self.tfidf)
        sorted_indices = sim.argsort()[0][::-1]        # get sorted indices and reverse them

        matches = []
        for i in range(k):
            matches.append({
                'doc_name': self.doc_name_list[sorted_indices[i]],
                'similarity_score': sim[0][i],
                'tfidf_vector': self.tfidf[sorted_indices[i]].todense().tolist()
            })

        return matches
