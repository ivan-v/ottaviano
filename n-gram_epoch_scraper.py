import json
import math
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
if ngrams[18].isdigit():
    n = int(ngrams[17:19])
else:
    n = int(ngrams[17])

input_file = open(ngrams)
output_file = open("unique-" + str(n) + "-grams_epochs.json", 'w')

count = 0
current_sequence = 0
temp_frequencies = {}
epochs = {}

for i, line in enumerate(input_file):

    current_sequence = list(map(int, line.split()[0:n]))
    
    year = int(line.split()[n])
    floored = math.floor(year/50)*50
    epoch = str(floored)+"-"+str(floored+49)
    
    if epoch not in epochs:
        epochs[epoch] = {}
    if str(tuple(current_sequence)) not in epochs[epoch]:
        epochs[epoch][str(tuple(current_sequence))] = int(line.split()[n+1])
    else:
        epochs[epoch][str(tuple(current_sequence))] += int(line.split()[n+1])

    count += 1
    if debug and count % 10000 == 0:
        print(count, " lines parsed so far.")

if debug:
    print("Writing to", str("unique-"+str(n)+"-grams_epochs.json..."))

json.dump(epochs, output_file, indent=2)

if debug:
    print(count, " lines parsed, ", len(epochs), " distinct eras collected.")