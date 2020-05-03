import json
import os
import sys
import operator

import matplotlib.pyplot as plt
'''
This is a simple epoch estimator! It takes a melody and a number of years to span from
standard input and calculates the most likely era (under the given span) that the given
melody came from. This is done by simply calculating the likelihood that the melody occurs
within each epoch in the dataset, storing the results, and then picking the epoch with
the highest probability.

For the graph, it requires matplotlib to be installed through pip or homebrew.

This program expects a file matching the input request to already exist: if you query with
a 3-gram melody and a 50 year span, there must be a file unique-3grams_epochs_50.json 
present in the folder /unique_ngrams_epochs/50/. Eventually each possibility should be built out
to accept a wide range of queries, but for testing purposes be mindful of your queries.

An example run of this program would be as follows:
run: python3 epoch_estimate.py
Enter 1 1 1      
Enter 50

There is an optional -debug flag that prints out all epoch probabilities. Simply add it
to the program call: python3 epoch_estimate.py -debug

'''

#check for debug flag
debug = len(sys.argv) > 1 and sys.argv[1] == "-debug"

#get melody and epoch range from user
print("Enter a melody for an epoch estimation.")
melody_input = input().split()
print("Enter a range of years to search by.")
epoch_size = input()

#get number of grams in melody to open corresponding data file
gram_count = str(len(melody_input))
unique_ngrams_folder = os.path.join("unique_ngrams_epochs", epoch_size)
n_grams = open(os.path.join(unique_ngrams_folder, "unique-"+gram_count+"-grams_epochs_"+epoch_size+".json"))
data = json.load(n_grams)

#convert input melody to match format of data files
melody = "("
for i in range(0,len(melody_input)):
    melody = melody + melody_input[i]
    if(i < len(melody_input)-1):
        melody = melody + ", "
melody = melody + ")"

#get average number of melodies contained in epochs
#also get min and max melody counts for debugging
melodies_sum = 0
epoch_count = 0
min_melodies = 2000000
max_melodies = 0
for epoch in data:
    melodies_sum += data[epoch][0]
    epoch_count += 1
    if(data[epoch][0] < min_melodies):
        min_melodies = data[epoch][0]
    if(data[epoch][0] > max_melodies):
        max_melodies = data[epoch][0]
average_melody_count = melodies_sum/epoch_count
if debug:
    print("Minimum melody count:", min_melodies)
    print("Maximum melody count:", max_melodies)
    print("Average melody count:", average_melody_count)
    

#iterate through data file and calculate probability of melody in each epoch
epoch_probabilities = {}
for epoch in data:
    total_melodies = data[epoch][0]
    temp_epoch_data = data[epoch][1]
    confidence = min(1/(average_melody_count/total_melodies),1.000)
    try:
        temp_melody_freq = temp_epoch_data[melody]
        temp_prob = temp_melody_freq/total_melodies
        epoch_probabilities[epoch] = temp_prob * confidence
        if debug:
            print(epoch, ": " , temp_prob, " confidence:",round(confidence,3))
        pass
    except KeyError:
        epoch_probabilities[epoch] = 0
        if debug:
            print(epoch, ": " , 0.0) 
        pass

#get key (epoch) with highest value (probability)
epoch_estimate = max(epoch_probabilities.items(), key=operator.itemgetter(1))[0]

print("This melody is most likely from the era:", epoch_estimate)
print(epoch_probabilities)

# Sorting the epochs chronologically
graph_input = {}
for key in sorted(epoch_probabilities.keys()):
    graph_input[key] = epoch_probabilities[key]

# making the graph
names = list(graph_input.keys())
values = list(graph_input.values())

fig, axs = plt.subplots(1, figsize=(18, 3), sharey=True)
# axs[0].bar(names, values)
# axs[1].scatter(names, values)
sequence = tuple(map(int, melody_input))
print(sequence)
fig.suptitle("Frequency of " + str(sequence))
axs.bar(names, values)
plt.show()