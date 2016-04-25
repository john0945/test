import glob
import re
from operator import itemgetter
from itertools import *


# below function taken from StackOverflow answer by Martijn Pieters http://stackoverflow.com/questions/16974047/efficient-way-to-find-missing-elements-in-an-integer-sequence
def missing_elements(L):

    start, end = L[0], L[-1]

    if L.len() > 0:
        return sorted(set(range(start, end + 1)).difference(L))

    else:
        return 0

files = glob.glob('./*.txt')

log = open("log.py", 'a')

for f in files:
    with open(f, 'r') as file:
        seq = []
        for line in file:
            seq_pos = line.find("seq")
            seq_line = [int(s) for s in re.findall(r'\d+', line[seq_pos:seq_pos + 10])]
            seq.append(seq_line[0])

        log.write("The missing packets in {} are {} \n".format(f[2:-4], missing_elements(seq)))

log.close()
