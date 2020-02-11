find_namespace:
	python3 expressions.py $(cat all_vocabs.csv | fzf | awk -F, '{print $2}')

check_unique_terms:
	cat /tmp/namespace_unique.csv | fzf 

check_triplets:
	cat /tmp/namespace.csv | fzf

lod_data:
	./get_lod_data.sh
