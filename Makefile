all: directories data feature_vectors

directories: 
	mkdir -p reuters-dataset
	mkdir -p feature-vectors
	mkdir -p wordcounts
	touch feature-vectors/tfidf_feature_vectors.csv

data:
	wget -r --no-parent -A "*.sgm" http://web.cse.ohio-state.edu/~srini/674/public/reuters/ 
	find web.cse.ohio-state.edu/~srini/674/public/reuters/ -name '*.sgm' -exec mv {} reuters-dataset/ \;
	rm -rf web.cse.ohio-state.edu

feature_vectors:
	python word_counter.py
	python count_feature_creator.py
	python tfidf_feature_creator.py
	python histogramer.py

clean:
	rm -rf reuters-dataset
	rm -rf feature-vectors
	rm -rf wordcounts
	rm *.pyc
