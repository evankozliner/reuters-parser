all: make_directories get_data 

make_directories: 
	mkdir -p reuters-dataset
	mkdir -p feature-vectors
	mkdir -p wordcounts

get_data:
	wget -r --no-parent -A "*.sgm" http://web.cse.ohio-state.edu/~srini/674/public/reuters/ 
	find web.cse.ohio-state.edu/~srini/674/public/reuters/ -name '*.sgm' -exec mv {} reuters-dataset/ \;
	rm -rf web.cse.ohio-state.edu

clean:
	rm -rf reuters-dataset
	rm -rf feature-vectors
	rm -rf wordcounts
