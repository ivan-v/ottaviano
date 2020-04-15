import json
import os
import sys

from ast import literal_eval # to convert a string of a tuple to tuple proper

# To run this, call n-gram_predicter.py unique-12-grams.json (or similar),
# as output from n-gram_scraper.py. It will create a 
# dictionary of a list of a sequence, which is of n-1 length, 
# and give it a list of dictionaries which is all that the next pitch could be,
# and what is its probability. 

# So the output matches this style:
# { epoch_1: [
#             (sequence_1): { potential_pitch_1: probability_1, potential_pitch_2, ...),
#             (sequence_2): {...},
#             ...
#            ]
#  epoch_2: [...]
# ...}

# The output file is named 12-grams-epoch_hmm.json (or however many n's we are).

# There's an optional flag of -debug prints every 10000 input lines read,
# and the finishing message. It goes after the input-file name:
# n-gram_scraper.py unique-12-grams.json -debug

ngrams = sys.argv[1]
debug = len(sys.argv) > 2 and sys.argv[2] == "-debug"

# determining what the n-count is from the file name
n = int("".join([str(i) for i in list(ngrams) if i.isdigit()]))

if not os.path.isdir("epoch_hmm"):
    os.makedirs("epoch_hmm")


destination = os.path.join("epoch_hmm", str(n) + '-grams-' + 'epoch_hmm.json')
output_file = open(destination, 'w')
input_file = open(ngrams)

data = json.load(input_file)
output = {}
sublocal_counts = 0
count = 0

for epoch in data:
    current = 0
    previous = 0
    local_counts = 0
    temp_probabilities = {}
    markov = {}
    for entry in data[epoch][1]:

        sequence = literal_eval(entry)
        current = sequence[0:n-1]

        if count == 0:
            previous = current

        if current == previous:
            temp_probabilities[sequence[n-1]] = data[epoch][1][entry]
        else:
            for probability in temp_probabilities:
                temp_probabilities[probability] = temp_probabilities[probability]/local_counts
            markov[str(previous)] = temp_probabilities
            temp_probabilities = {}
            previous = current
            temp_probabilities[sequence[n-1]] = data[epoch][1][entry]
            local_counts = 0
        local_counts += data[epoch][1][entry]
        count += 1
    output[epoch] = markov
    
    if debug:
        print("Epoch " + epoch + " has been completed.")

if debug:
    print("Writing to ", (str(str(n) + '-grams-' + 'epoch_hmm.json' + "...")))

json.dump(output, output_file, indent=2)

if debug:    
    print(count, "lines parsed,", len(data), "epochs for", str(n), "-grams saved.")