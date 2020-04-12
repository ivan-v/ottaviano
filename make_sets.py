import sys
import random
import os

'''
To run this, cal make_sets.py <path/to/original/data>. It will create three
new files: training_n-gram.csv, dev_n-gram.csv, and test_n-gram.csv. These files will be added
to a folder called sets (in the git tree) and should be referenced from there for their 
perspective duties (meaning there is no need to perform tasks on the original data - these
files should be used instead from now on).

Since Github's data storage limit is 100MB per file, I will start by creating 
sets for n-grams 1 through 3. We can start working with those and put more in the
google drive as needed. At some point if we want to have sets for all n-grams we will need to store them locally 
and make sure we do not alter them, but for now this should be fine.

Further, if it is ever useful to combine multiple n-gram counts into a single set (ie a 
training set containing all data from n-grams 1 - 3) that would be trivial! We can decide 
what we need as we go.
'''

ngrams = sys.argv[1]
debug = len(sys.argv) > 2 and sys.argv[2] == "-debug"

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

if debug:
    print("Debug On")
    print("Reading from file: " + ngrams)


input_file = open(ngrams)
#filename = os.path.join(fileDir, 'data/same.txt')
training_output = open("./sets/training_" + str(n) + "-grams.csv", 'w')
dev_output = open("./sets/dev_" + str(n) + "-grams.csv", 'w')
test_output = open("./sets/test_" + str(n) + "-grams.csv", 'w')

#get total num of lines in file
num_lines = sum(1 for lines in input_file)
input_file.seek(0)

# get desired sizes for each set
test_size = int(num_lines * .10) # %10 for test
dev_size = int(num_lines * .20)  # %20 for dev
# remaining %70 will be for training

#get random distribution of indices
random_all = random.sample(range(0, num_lines-1), test_size+dev_size)

#split random indices for each set we need
#store in dictionaries for fast lookup times later
random_test = {}
for i in range(0,test_size):
    random_test[random_all[i]] = 1

random_dev = {}
for i in range(test_size,len(random_all)):
    random_dev[random_all[i]] = 1

#iterate through file and put each line in its perspective set
for i, line in enumerate(input_file):
    if i in random_test:
        if debug and (i%1000 == 0):
            print("Writing to test set: ", i)
        test_output.write(line)
    elif i in random_dev:
        if debug and (i%1000 == 0):
            print("Writing to dev set: ", i)
        dev_output.write(line)
    else:
        if debug and (i%1000 == 0):
            print("Writing to training set: ", i)
        training_output.write(line)


input_file.close()
training_output.close()
dev_output.close()
test_output.close()