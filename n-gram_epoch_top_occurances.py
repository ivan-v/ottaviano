import json
import re
import sys

from ast import literal_eval # to convert a string of a tuple to tuple proper
from operator import itemgetter

# To run this, call n-gram_predicter.py unique-12-grams_epochs.json x
# (or whatever n-grams you're looking at) as output from 
# n-gram_epoch_scraper.py, where x is how many top sequences you want 
# to see for each epoch. It will create a dictionary of all the epochs,
# with a list of dictionaries of all the top sequences for each epoch,
# with each sequence having the value of its frequency.

# The sequences are sorted from most to least frequent.

# The output file is named 12-grams_top-x.json (or however many n's we are),
# where x is the number of sequences for each epoch.

ngrams = sys.argv[1]
top = int(sys.argv[2])
debug = len(sys.argv) > 3 and sys.argv[3] == "-debug"

# determining what the n-count is from the file name
n = int("".join([str(i) for i in list(ngrams) if i.isdigit()]))

output_file = open(str(str(n) + '-grams' + '_top-' + str(top) + '.json'), 'w')
input_file = open(ngrams)

data = json.load(input_file)

most_common = {}

for epoch in data:
    res = dict(sorted(data[epoch][1].items(), key = itemgetter(1), reverse = True)[:top])
    most_common[epoch] = res

json.dump(most_common, output_file, indent=2)