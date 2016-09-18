# reuters-parser

*The project is split up into several parts: To see the full functionality run them in this order*

1. *The Makefile:* Downloads the data and makes the necessary directories. Run using `make`

2. *The wordcount file generator:* Writes the `final_wordcount.csv` file which is used to take words b etween some frequency range. Run using `python word_counter.py`

3. *The histogramer:* Displays an image of the 'long tail' graph associated with the corpus. Run using `python histogramer.py`. The histogram can be used to interpret what range of word frequency to use.

4. *The word count feature vector builder:* Builds a feature vector of the word counts per document between some range of word based on frequency. Run using `python count_feature_creator.py`. Writes the feature vector to `feature-vectors/wordcount_feature_vectors.csv`

5. *The TF/IDF feature vector builder:* Builds a feature vector based on the TF/IDF ratio per document. Writes the resulting feature vector to `feature-vectors/tfidf_feature_vectors.csv`
