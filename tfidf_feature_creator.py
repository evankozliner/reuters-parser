from sklearn.feature_extraction.text import TfidfVectorizer
import os
from reuters_parser import ReutersParser
import csv

DATA_DIR = "reuters-dataset/"
OUTPUT_FILE = "feature-vectors/tfidf_feature_vectors.csv"

def create_tfidf_training_data(docs):
    y = [d[0] for d in docs]
    corpus = [d[1] for d in docs]
    vectorizer = TfidfVectorizer(min_df=1)
    x = vectorizer.fit_transform(corpus)
    return x, y

def record_vector(x,y):
    Y = [reduce(lambda a,b: a + "|" + b, labels) if len(labels) > 0 else "None" for labels in y]
    with open(OUTPUT_FILE, 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        for i in xrange(len(Y)):
            row = [Y[i]] + x[i].toarray().tolist()
            writer.writerow(row)

def main():
    parser = ReutersParser()
    files = os.listdir(DATA_DIR)
    count = 0.0
    for filename in files:
        docs = list(parser.parse(open(DATA_DIR + filename, 'rb')))
        x, y = create_tfidf_training_data(docs)
        record_vector(x,y)
        count += 1
        print str(count/len(files)) + "% complete"

if __name__ == "__main__":
    main()
