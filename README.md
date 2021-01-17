# Ottaviano
## A Computational Music Analysis research project
A method of analyzing sheet music through n-grams and Hidden Markov models to observe stylistic differences 
throughout time.

## Authors
Ivan Viro & Paul Odenwaldt, 2020

## Running the Program

### Overhead:

First, make sure that you have n-gram csv files, as found
in http://www.peachnote.com/datasets.html

Then, decide on how wide the epoch categories to be (i.e. sort
by 25, 50, 100 years, etc.). 

The ```-debug``` flag is available for every following program call as 
an optional final parameter, and it will print progress of the 
running program.

When ready, call 
    ```n-gram_epoch_scraper.py *.csv x```
from where the n-gram csv files are,
and with x being the epoch width (a natural number).

After that finishes, call 
    ```n-gram_epoch_predicter.py *.json```
for where your unique_n-grams are (which are generated from n-gram_epoch_scraper.py, and are by default in a folder
called unique_n-grams\\x).

This is the end of the overhead. Now the following become available:

### As an tool for analysis
To see in which epochs a given melody appears most often in:
    ```epoch_estimate.py [enter sequence as integers seperated by spaces, like "1 1 1"]
    [enter epoch-length, like "50"]```

_NOTE: this requires matplotlib and pandas to be installed._


To generate a melody probabilistically from a given epoch:

    ```melody_generator_epoch.py 1750-1799 -debug``` 
(or any vailable epoch)
_NOTE: this requires numpy, midi, fluidsynth, and FluidR3_GM.sf2 to be installed.
The more likely that a melody appears in that epoch, the more
likely it is that it will be generated. Less-common epochs 
may generate shorted melodies, and this is expected._


To see the top z melodic sequences which appear in a given n-gram length (where z = 100 for top 100, etc.):
```n-gram_predicter.py unique-12-grams_epochs.json z```  