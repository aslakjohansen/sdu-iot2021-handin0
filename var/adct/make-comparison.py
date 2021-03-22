#!/usr/bin/env python3

# time ./make-heatmap ~/vcs/git/serial-logger/src/log.csv heatmap.json

from sys import argv, exit 
import json

sep = ','
X_COLUMN = 2
Y_COLUMN = 1
T_COLUMN = 2 # for comparing t0 and t1 against

###############################################################################
########################################################################## main

# guard: command line arguments
if len(argv)!=5:
    print('Syntax: %s CSV_FILENAME JSON_FILENAME T0 T1' % argv[0])
    print('        %s adct4.log polylines.csv 16831 19965' % argv[0])
    exit(1)
input_filename  =     argv[1]
output_filename =     argv[2]
t0              = int(argv[3])
t1              = int(argv[4])

# process data
first = True
lines = [] #['#index,device_time,laptop_time']
with open(input_filename) as fo:
    for line in fo:
        line = line.strip()
        if len(line)==0: continue
        if line[0]=='#': continue
        
        parts = line.split(sep)
        
        if len(parts)!=4:
            print('Error parsing line "%s".' % line)
            continue
        
        value = float(parts[Y_COLUMN])*1000
        time  = int(  parts[X_COLUMN])
        t     = int(  parts[T_COLUMN])
        
        if first:
            i = 0
            time0  = time
            value0 = value
            first = False
        
        if t>=t0 and t<=t1:
            lines.append(','.join(map(lambda entry: str(entry), [i, time-time0, value-value0])))
            i += 1

# write result to disk
with open(output_filename, 'w') as fo:
    fo.writelines(map(lambda line: line+'\n', lines))

