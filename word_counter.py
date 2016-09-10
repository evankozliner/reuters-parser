""" Main file for the article parser. 
    Evan Kozliner
""" 

import os
from reuters_parser import ReutersParser
import pprint
import string
import csv

DATA_DIR = "reuters-dataset/"

def main():
    #for f in os.listdir(DATA_DIR):
    word_count_mapping = {}
    parser = ReutersParser()
    for f in ["reut2-018.sgm", "reut2-000.sgm"]:
        with open(DATA_DIR + f) as data:
            doc = parser.parse(data)
            word_count_mapping = build_word_count_hash(doc, word_count_mapping)
    write_csv_from_hash(sorted(word_count_mapping.items(), key = lambda x: x[1]))

def build_word_count_hash(doc, word_count_mapping):
    """ Returns a hash mapping words count to their count """
    for article in doc:
        for raw_word in article[1].split():
            exclude = set(string.punctuation)
            word = ''.join(ch for ch in raw_word if ch not in exclude)
            if word in word_count_mapping.keys():
                word_count_mapping[word] += 1
            else:
                word_count_mapping[word] = 1
    return word_count_mapping

def write_csv_from_hash(word_mapping):
    """ Write a CSV containing words and their cross-article counts """
    with open('words_to_count.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        for pair in word_mapping:
            writer.writerow([pair[0], pair[1]])
            
if __name__ == "__main__":
    main()
