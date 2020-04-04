import json
import re
import sys

from ast import literal_eval # to convert a string of a tuple to tuple proper

# To run this, call n-gram_predicter.py unique-12-grams.json (or similar),
# as output from n-gram_scraper.py. It will create a 
# dictionary of a list of a sequence, which is of n-1 length, 
# and give it a list of dictionaries which is all that the next pitch could be,
# and what is its probability. 

# So the output matches this style:
# {(sequence_1): [{potential_pitch_1:probability}, {potential_pitch_2, probability}]),
#  (sequence_2): [{potential_pitch_1:probability}, ...],
# ...}

# The output file is named 12-grams-hmm.json (or however many n's we are).

# There's an optional flag of -debug prints every 10000 input lines read,
# and the finishing message. It goes after the input-file name:
# n-gram_scraper.py unique-12-grams.json -debug

ngrams = sys.argv[1]
debug = len(sys.argv) > 2 and sys.argv[2] == "-debug"

# determining what the n-count is from the file name
n = int("".join([str(i) for i in list(ngrams) if i.isdigit()]))

output_file = open(str(str(n) + '-grams-' + 'hmm.json'), 'w')
input_file = open(ngrams)


data = json.load(input_file)
count = 0
current = 0
previous = 0
markov = {}
temp_probabilities = []
local_counts = 0

for entry in data.items():
    
    sequence = literal_eval(entry[0])
    current = sequence[0:n-1]

    if count == 0:
        previous = current

    if current == previous:
        temp_probabilities.append({sequence[n-1]: entry[1]})
    else:
        for probability in temp_probabilities:
            for tone in probability:
                probability[tone] = probability[tone]/local_counts
        markov[str(previous)] = temp_probabilities
        previous = current
        temp_probabilities = [{sequence[n-1]: entry[1]}]
        local_counts = 0
    local_counts += entry[1]
    count += 1
    if debug and count % 10000 == 0:
        print(count, " lines parsed so far.")

json.dump(markov, output_file, indent=2)

if debug:    
    print(count, " lines parsed, ", len(markov), " unique", str(n), "-grams saved.")