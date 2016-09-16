import matplotlib.pyplot as plt
import csv
import scipy
import random

#WORDCOUNT_FILE = "wordcounts/reut2-000.sgm_wordcount.csv"
WORDCOUNT_FILE = "final_wordcount.csv"

def get_rand_colors(x):
    r = lambda: random.randint(0,225)
    return ['#%02X%02X%02X' % (r(), r(), r()) for color in range(x)]

def show_bar_graph_by_hash(h, xlabel, ylabel):
    x = scipy.arange(len(h))
    sorted_words = sorted(h.keys(), key = lambda word: h[word])
    labels = [s.encode('utf-8') for s in sorted_words]
    y = scipy.array([h[s] for s in labels])
    color_list = get_rand_colors(len(h))
    plt.bar(x,y,color=color_list)
    plt.xticks(x,labels)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def main():
    with open(WORDCOUNT_FILE, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        wordcount_map = {}
        for row in reader:
            wordcount_map[row[0]] = int(row[1])
        wordcount_map = {k: v for k,v in wordcount_map.items() if v > 500}
        show_bar_graph_by_hash(wordcount_map, "word", "count")

if __name__ == "__main__":
    main()

