import sys
import csv
import string
import os
import nltk
from reuters_parser import ReutersParser
import word_counter

MIN_CORPUS_COUNT = 100
MAX_CORPUS_COUNT = 5000
OUTPUT_FILE = "feature-vectors/wordcount_feature_vectors.csv"
DATA_DIR = "reuters-dataset/"
WORDCOUNT_FILE = "final_wordcount.csv"

def get_word_features():
    features = []
    with open(WORDCOUNT_FILE) as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            if int(row[1]) < MAX_CORPUS_COUNT and int(row[1]) > MIN_CORPUS_COUNT:
                features.append(row[0])
    return features

def write_feature_vectors(data, features, parser):
    doc = parser.parse(data)
    stemmer = nltk.stem.SnowballStemmer("english")
    with open(OUTPUT_FILE, 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(features)
        for article in doc:
            write_feature_vector(stemmer, article, features, writer)

# TODO Optimize me
def write_feature_vector(stemmer, article, features, writer):
    feature_vector = [0 for x in features]
    for raw_word in article[1].split():
        exclude = set(string.punctuation)
        word = stemmer.stem(''.join(ch for ch in raw_word if ch not in exclude))
        if word in features:
            feature_vector[features.index(word)] += 1
    writer.writerow(feature_vector)

def main():
    print "Generating word count vector for words appearing in the corpus between " + \
            str(MIN_CORPUS_COUNT) + " and " + str(MAX_CORPUS_COUNT)
    features = get_word_features()
    count = 0.0
    parser = ReutersParser()
    for f in [os.listdir(DATA_DIR)[0]]:
        with open(DATA_DIR + f) as data:
            print "Writing training data from " + f
            write_feature_vectors(data, features, parser)

if __name__ == "__main__":
    main()
