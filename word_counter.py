""" Main file for the article parser. 
    Evan Kozliner
""" 

import os
from reuters_parser import ReutersParser
import pprint
import string
import csv
import nltk

DATA_DIR = "reuters-dataset/"
OUTPUT_DIR = "wordcounts/"
FINAL_DATA_FILENAME = "final"

def main():
    parser = ReutersParser()
    already_parsed = map(lambda s: s[:-14], os.listdir(OUTPUT_DIR))
    files = filter(lambda f: f not in already_parsed, os.listdir(DATA_DIR))
    count = 0.0
    for f in files:
        with open(DATA_DIR + f) as data:
            doc = parser.parse(data)
            word_count_mapping = build_word_count_hash(doc)
            #write_csv_from_hash(sorted(word_count_mapping.items(), key = lambda x: x[1]), \
            #        OUTPUT_DIR + f)
            write_csv_from_hash(word_count_mapping, OUTPUT_DIR + f)
        count += 1
        print str(count / float(len(files))) + "% complete."
    write_aggregate_csv()

def write_aggregate_csv():
    """ 
    Combines the already written CSV's into a larger one to avoid memory constraints 
    """
    print "Combining smaller CSV's into final wordcount..."
    final_hash = {}
    files = os.listdir(OUTPUT_DIR)
    count = 0.0
    final_words = set()
    for f in files:
        with open(OUTPUT_DIR + f) as data:
            reader = csv.reader(data)
            for row in reader:
                if row[0] in final_words:
                    final_hash[row[0]] += int(row[1])
                else:
                    final_words.add(row[0])
                    final_hash[row[0]] = int(row[1])
        count += 1
        print str(count/float(len(files))) + "% complete"
    write_csv_from_hash(dict(sorted(final_hash.items(), key = lambda x: x[1])), FINAL_DATA_FILENAME)

def build_word_count_hash(doc):
    """ Returns a hash mapping stemmed words count to their count """
    word_count_mapping = {}
    existing_words = set() # Slight optimization as pythons dict.keys() method returns list
    stemmer = nltk.stem.SnowballStemmer("english")
    for article in doc:
        for raw_word in article[1].split():
            exclude = set(string.punctuation)
            word = stemmer.stem(''.join(ch for ch in raw_word if ch not in exclude))
            if word in existing_words:
                word_count_mapping[word] += 1
            else:
                existing_words.add(word)
                word_count_mapping[word] = 1
    return word_count_mapping

def write_csv_from_hash(word_mapping, corresponding_filename):
    """ Write a CSV containing words and their cross-article counts """
    with open(corresponding_filename + '_wordcount.csv', 'w+') as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        for key in word_mapping:
            try:
                writer.writerow([key, word_mapping[key]])
            except UnicodeError:
                print("Unicode err, ignoring sample")
            
if __name__ == "__main__":
    main()
