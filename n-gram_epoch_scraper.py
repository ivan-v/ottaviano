import json
import math
import os
import sys

from glob import glob # to process/run on many files

# To run this, simply call n-gram_scraper.py *.csv x for where your n-grams are
# (for example, on Windows: py n-gram_scraper.py .\ngrams\*.csv 50) 
# to process all of them, and where x in the command-line input is the length of the epochs
# in years (i.e, 50 -> categorizing into half-centuries)

# Alternatively, you can process an individual melodic csv n-gram file as well, in the format
# which it appears in http://www.peachnote.com/datasets.html
# It will write to unique-4-grams_epochs.json, (or whatever n-values we are looking at),
# in a directory/folder of "unique_ngrams_epochs" with counts of 
# each sequence in that epoch from all the relevant years found in the csv.

# There's an optional flag of -debug prints every 10000 input lines read,
# and the finishing message. It goes after the input-file name:
# n-gram_scraper.py .\imslp-interval-12gram-20110401.csv -debug

def ls(fname):
    # Returns either [fname] or a list of the contents of fname if fname is a
    # directory.  On Windows only, expands globs (e.g., *.csv) before listing
    # fname.
    fnames = glob(fname) if os.name == 'nt' else [fname]
    lists = [os.listdir(f) if os.path.isdir(f) else [f] for f in fnames]
    return [f for fs in lists for f in fs]

def main():
    fnames = [f for fs in map(ls, sys.argv[1:]) for f in fs]
    if sys.argv[-1] != '-debug':
        epoch_length = int(sys.argv[-1])
    else:
        epoch_length = int(sys.argv[-2])
    for fname in fnames:
        print("Processing {}...".format(fname), file=sys.stderr)
        process_csv(fname, epoch_length)

def process_csv(fname, epoch_length):
    ngrams = fname
    debug = len(sys.argv) > 3 and sys.argv[3] == "-debug"

    # determining what the n-count is from the file name
    n = int("".join("".join([str(i) for i in list(ngrams) if i.isdigit()]).split("20110401")))

    if not os.path.isdir("unique_ngrams_epochs"):
        os.makedirs("unique_ngrams_epochs")

    if not os.path.isdir(os.path.join("unique_ngrams_epochs", str(epoch_length))):
        os.makedirs(os.path.join("unique_ngrams_epochs", str(epoch_length)))

    input_file = open(ngrams)
    file_name = "unique-"+str(n)+"-grams_epochs_"+str(epoch_length)+".json"
    destination = os.path.join("unique_ngrams_epochs", str(epoch_length), file_name)
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
        floored = math.floor(year/epoch_length)*epoch_length
        epoch = str(floored)+"-"+str(floored+epoch_length-1)
        
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
        print("Writing to", os.path.join(str(epoch_length), file_name))

    json.dump(epochs, output_file, indent=2)

    if debug:
        print(count, " lines parsed, ", len(epochs), " distinct eras collected.")

if __name__ == '__main__':
    main()