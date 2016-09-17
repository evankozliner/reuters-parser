all: make_directories get_data 

make_directories: 
	mkdir -p reuters-dataset
	mkdir -p feature-vectors
	mkdir -p wordcounts

get_data:
	wget -r -A "*.sgm" http://web.cse.ohio-state.edu/~srini/674/public/reuters/

clean:
	rm -rf reuters-dataset
	rm -rf feature-vectors
	rm -rf wordcounts
