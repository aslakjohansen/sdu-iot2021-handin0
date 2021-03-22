#!/usr/bin/env python3

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

filename = 'timediff.csv'

# get number of samples
with open(filename) as fo:
    linecount = len(fo.readlines())

plt.figure(figsize=[6.5,4])
df = pd.read_csv(filename, names=['laptop', 'laptopdiff', 'device', 'devicediff'])
plot = sns.histplot(df, x=df['devicediff'], stat="count", kde=False, binwidth=1)
plt.xlabel('Time/[ms]')
plt.ylabel('Occurences/[]')
plt.title('Sampling Periods From Device (%u Repetitions)' % linecount)
plt.savefig('timediff.pdf')
