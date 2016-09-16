""" Main file for the article parser. 
    Evan Kozliner
""" 

import os
from reuters_parser import ReutersParser
import pprint
import string
import csv

# TODO put wget in make

DATA_DIR = "reuters-dataset/"
OUTPUT_DIR = "wordcounts/"
FINAL_DATA_FILENAME = "final"

def main():
    parser = ReutersParser()
    already_parsed = map(lambda s: s[:-14], os.listdir(OUTPUT_DIR))
    files = filter(lambda f: f not in already_parsed, os.listdir(DATA_DIR))
    count = 0.0
    for f in files:
        print "Parsing file: " + f
        with open(DATA_DIR + f) as data:
            doc = parser.parse(data)
            word_count_mapping = build_word_count_hash(doc)
            write_csv_from_hash(sorted(word_count_mapping.items(), key = lambda x: x[1]), \
                    OUTPUT_DIR + f)
        count += 1
        print "Finished parsing file: " + f
        print str(count / float(len(files))) + "% complete."
    write_aggregate_csv()

def write_aggregate_csv():
    final_hash = {}
    files = os.listdir(OUTPUT_DIR)
    count = 0.0
    for f in files:
        with open(OUTPUT_DIR + f) as data:
            reader = csv.reader(data)
            for row in reader:
                if row[0] in final_hash.keys():
                    final_hash[row[0]] += int(row[1])
                else:
                    final_hash[row[0]] = int(row[1])
        count += 1
        print str(count/float(len(files))) + "% complete"
    write_csv_from_hash(sorted(final_hash.items(), key = lambda x: x[1]), FINAL_DATA_FILENAME)

def build_word_count_hash(doc):
    """ Returns a hash mapping words count to their count """
    word_count_mapping = {}
    for article in doc:
        for raw_word in article[1].split():
            exclude = set(string.punctuation)
            word = ''.join(ch for ch in raw_word if ch not in exclude)
            if word in word_count_mapping.keys():
                word_count_mapping[word] += 1
            else:
                word_count_mapping[word] = 1
    return word_count_mapping

def write_csv_from_hash(word_mapping, corresponding_filename):
    """ Write a CSV containing words and their cross-article counts """
    with open(corresponding_filename + '_wordcount.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        for pair in word_mapping:
            try:
                writer.writerow([pair[0], pair[1]])
            except UnicodeError:
                print("Unicode err, ignoring sample")
            
if __name__ == "__main__":
    main()
