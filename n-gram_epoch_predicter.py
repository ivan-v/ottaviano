import json
import os
import sys

from ast import literal_eval # to convert a string of a tuple to tuple proper
from glob import glob # to process/run on many files

# To run this, simply call n-gram_epoch_predicter.py *.json for where your 
# unique_n-grams are (which are generated from n-gram_epoch_scraper.py).
# For example, on Windows: py n-gram_scraper.py .\unique_ngrams_epochs\*.json)
# to process all of them. 
# Alternatively, you can process an individual unique-n-grams_epochs.json file as well.
# It will write to n-grams_epochs_hmm.json, (or whatever n-values we are looking at),
# in a directory/folder of "epochs_hmm"

# It expects unique_ngrams_epochs\epoch_length\*.json (where epoch_length is a number,)
# like 100 for every century, etc.)

# It will create a dictionary of a list of a sequence, which is of n-1 length, 
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

def ls(fname):
    # Returns either [fname] or a list of the contents of fname if fname is a
    # directory.  On Windows only, expands globs (e.g., *.hson) before listing
    # fname.
    fnames = glob(fname) if os.name == 'nt' else [fname]
    lists = [os.listdir(f) if os.path.isdir(f) else [f] for f in fnames]
    return [f for fs in lists for f in fs]

def main():
    fnames = [f for fs in map(ls, sys.argv[1:]) for f in fs]
    for fname in fnames:
        print("Processing {}...".format(fname), file=sys.stderr)
        process_unique_ngrams(fname)

def process_unique_ngrams(fname):
    ngrams = fname
    debug = len(sys.argv) > 2 and sys.argv[2] == "-debug"

    # determining what the n-count is from the file name
    n = int("".join([str(i) for i in list(ngrams[len(ngrams)-29:len(ngrams)-10]) if i.isdigit()]))
    # determining time period/epoch lengths
    epoch_length = "".join([str(i) for i in list(ngrams[len(ngrams)-11:]) if i.isdigit()])

    if not os.path.isdir("epochs_hmm"):
        os.makedirs("epochs_hmm")

    if not os.path.isdir(os.path.join("epochs_hmm", epoch_length)):
        os.makedirs(os.path.join("epochs_hmm", epoch_length))


    output_name = str(n) + '-grams-' + 'epochs_hmm_' + epoch_length + '.json'
    destination = os.path.join("epochs_hmm", epoch_length, output_name)
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
        print("Writing to", output_name)

    json.dump(output, output_file, indent=2)

    if debug:    
        print(count, "lines parsed,", len(data), "epochs for", str(n), "-grams saved.")

if __name__ == '__main__':
    main()