#!/usr/bin/env python3

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

filename = 'adc_diff.log'

# get number of samples
with open(filename) as fo:
    linecount = len(fo.readlines())

plt.figure(figsize=[6.5,4])
df = pd.read_csv(filename, names=['start', 'diff', 'value'])
plot = sns.histplot(df, x=df['diff'], stat="density", kde=True, binwidth=0.001)
plt.xlabel('Time/[s]')
plt.ylabel('Occurences/[density]')
plt.title('Inter-Sample Time Measurements (%u Repetitions)' % linecount)
plt.savefig('hist.pdf')
