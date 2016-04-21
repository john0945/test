import glob
import re
from operator import itemgetter
from itertools import *

#below function taken from StackOverflow answer by Martijn Pieters http://stackoverflow.com/questions/16974047/efficient-way-to-find-missing-elements-in-an-integer-sequence
def missing_elements(L):
    start, end = L[0], L[-1]

    return sorted(set(range(start, end + 1)).difference(L))

files = glob.glob('./*.txt')

for f in files:
    with open(f, 'r') as file:
        seq = []
        for line in file:
            seq_pos = line.find("seq")
            seq_line = [int(s) for s in re.findall(r'\d+',line[seq_pos:seq_pos+10])]
            seq.append(seq_line[0])

        print("The missing packets in {} are {}".format(f[2:-4],  missing_elements(seq)))
        #
        # list = []
        #
        # for k, g in groupby(enumerate(seq), lambda (i,x):i-x):
        #     list.append(map(itemgetter(1), g))
