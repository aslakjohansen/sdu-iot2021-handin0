#!/usr/bin/env python3

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=[6.5,4])
df = pd.read_csv('comparison.csv', names=['index', 'device', 'laptop'])
plot1 = sns.lineplot(x=df['index'], y=df['device'], marker='o')
plot2 = sns.lineplot(x=df['index'], y=df['laptop'], marker='o')
plt.legend(loc='upper left', labels=['Device', 'Laptop'])
plt.xlabel('index/[]')
plt.ylabel('Time/[ms]')
plt.savefig('comparison.pdf')
