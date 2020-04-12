import json
import sys


# To run this, simply call n-gram_scraper.py .\imslp-interval-12gram-20110401.csv
# (or any other interval n-gram file). It will write to data.json, 
# making a dictionary of unique n-grams, 
# which counts them from all years found in the csv.

# There's an optional flag of -debug prints every 10000 input lines read,
# and the finishing message. It goes after the input-file name:
# n-gram_scraper.py .\imslp-interval-12gram-20110401.csv -debug

ngrams = sys.argv[1]
debug = len(sys.argv) > 2 and sys.argv[2] == "-debug"


# determining what the n-count is from the file name
# if ngrams[18].isdigit():
#     n = int(ngrams[17:19])
# else:
#     n = int(ngrams[17])

#this is another way of determining n-count from input file name
#which allows for files to be in a different directory/be called
#in different ways (ie ./imslp-interval-12gram-20110401.csv instead
# of .\imslp-interval-12gram-20110401.csv)
i = 0
tempStr = ngrams[i:i+5]
while tempStr != "imslp":
    i = i + 1
    tempStr = ngrams[i:i+5]

if ngrams[16 + i].isdigit():
    n = int(ngrams[15+i:17+i])
else:
    n = int(ngrams[15+i])

input_file = open(ngrams)
output_file = open("unique-" + str(n) + "-grams.json", 'w')

count = 0
prev_sequence = 0
current_sequence = 0
sequence_frequency = {}
temp_frequency = 0

for i, line in enumerate(input_file):

    current_sequence = list(map(int, line.split()[0:n]))

    if count == 0:
        prev_sequence = current_sequence

    if current_sequence == prev_sequence:
        temp_frequency += int(line.split()[n+1])

    else:
        sequence_frequency[str(tuple(prev_sequence))] = temp_frequency
        prev_sequence = current_sequence
        temp_frequency = int(line.split()[n+1])

    count += 1
    if debug and count % 10000 == 0:
        print(count, " lines parsed so far.")


json.dump(sequence_frequency, output_file, indent=2)

if debug:
    print(count, " lines parsed, ", len(sequence_frequency), " unique ", str(n), "-grams saved.")