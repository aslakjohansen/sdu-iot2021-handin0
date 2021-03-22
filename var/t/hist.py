#!/usr/bin/env python3

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

filename = 't_processed.log'

# get number of samples
with open(filename) as fo:
    linecount = len(fo.readlines())

plt.figure(figsize=[6.5,4])
df = pd.read_csv(filename, names=['count', 'stime', 'itime'])
plot = sns.histplot(df, x=df['itime'], stat="count", kde=False, binwidth=1)
plt.xlabel('Time/[ns]')
plt.ylabel('Occurences/[]')
plt.title('Average Time per Timestamp Production (%u Repetitions)' % linecount)
plt.savefig('thist.pdf')
