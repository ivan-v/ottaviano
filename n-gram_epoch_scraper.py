import json
import math
import os
import sys


# To run this, simply call n-gram_scraper.py .\imslp-interval-12gram-20110401.csv
# (or any other interval n-gram file). It will write to unique-4-grams_epochs.json, 
# (or whatever n-value we are looking at),
# making a dictionary of epochs with counts of each sequence in that epoch
# from all the relevant years found in the csv.

# There's an optional flag of -debug prints every 10000 input lines read,
# and the finishing message. It goes after the input-file name:
# n-gram_scraper.py .\imslp-interval-12gram-20110401.csv -debug

ngrams = sys.argv[1]
debug = len(sys.argv) > 2 and sys.argv[2] == "-debug"

# determining what the n-count is from the file name
n = int("".join("".join([str(i) for i in list(ngrams) if i.isdigit()]).split("20110401")))

input_file = open(ngrams)
destination = os.path.join("unique_ngrams", "unique-"+str(n)+"-grams_epochs.json")
output_file = open(destination, 'w')

count = 0
current_sequence = 0
temp_frequencies = {}
epochs = {}
count_per_epoch = {}

for i, line in enumerate(input_file):

    current_sequence = list(map(int, line.split()[0:n]))
    frequency = int(line.split()[n+1])
    
    year = int(line.split()[n])
    floored = math.floor(year/50)*50
    epoch = str(floored)+"-"+str(floored+49)
    
    if epoch not in epochs:
        epochs[epoch] = {}
        count_per_epoch[epoch] = 0

    if str(tuple(current_sequence)) not in epochs[epoch]:
        epochs[epoch][str(tuple(current_sequence))] = frequency
        count_per_epoch[epoch] += frequency
    else:
        epochs[epoch][str(tuple(current_sequence))] += frequency
        count_per_epoch[epoch] += frequency 

    count += 1
    if debug and count % 10000 == 0:
        print(count, " lines parsed so far.")

for epoch in epochs:
    epochs[epoch] = (count_per_epoch[epoch], epochs[epoch])

if debug:
    print("Writing to", str("unique-"+str(n)+"-grams_epochs.json..."))

json.dump(epochs, output_file, indent=2)

if debug:
    print(count, " lines parsed, ", len(epochs), " distinct eras collected.")