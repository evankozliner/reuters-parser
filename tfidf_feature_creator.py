from sklearn.feature_extraction.text import TfidfVectorizer
import count_feature_creator
import os
from reuters_parser import ReutersParser
import csv
import nltk
import string

DATA_DIR = "reuters-dataset/"
OUTPUT_FILE = "feature-vectors/tfidf_feature_vectors.csv"

def strip_undesired_words(body, desired_features, stemmer): 
    stripped_body = "" # lol it's still a good name
    for raw_word in body.split():
        exclude = set(string.punctuation)
        word = stemmer.stem(''.join(ch for ch in raw_word if ch not in exclude))
        if word in desired_features: 
            stripped_body += word + " "
    return stripped_body

def filter_corpus_based_on_frequency(corpus):
    print "filtering corpus"
    desired_features = set(count_feature_creator.get_word_features())
    filtered_corpus = []
    stemmer = nltk.stem.SnowballStemmer("english")
    for body in corpus:
        filtered_corpus.append(strip_undesired_words(body, desired_features, stemmer))
    return filtered_corpus

def create_tfidf_training_data(docs):
    y = [d[0] for d in docs]
    corpus = [d[1] for d in docs]
    filtered_corpus = filter_corpus_based_on_frequency(corpus)
    vectorizer = TfidfVectorizer(min_df=1)
    print "Creating TF/IDF matrix"
    x = vectorizer.fit_transform(filtered_corpus)
    return x, y, map(lambda x: x.encode('utf-8'), vectorizer.get_feature_names())

def record_vector(x,y, header):
    print "Writing TF/IDF matrix to CSV. This can take several minutes depending on the ." + \
            " frequency range chosen in count_feature_creator."
    Y = [reduce(lambda a,b: a + "|" + b, labels) if len(labels) > 0 else "None" for labels in y]
    with open(OUTPUT_FILE, 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow([""] + header)
        for i in xrange(len(Y)):
            row = [Y[i]] + x[i].toarray().tolist()
            writer.writerow(row)
    print "Done!"

def main():
    parser = ReutersParser()
    files = os.listdir(DATA_DIR)
    count = 0.0
    docs = []
    print "Parsing sgms "
    for filename in files:
        docs = docs + list(parser.parse(open(DATA_DIR + filename, 'rb')))
    x, y, header = create_tfidf_training_data(docs)
    record_vector(x,y, header)

if __name__ == "__main__":
    main()
