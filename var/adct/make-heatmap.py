#!/usr/bin/env python3

# time ./make-heatmap ~/vcs/git/serial-logger/src/log.csv heatmap.json

from sys import argv, exit 
import json

sep = ','
X_COLUMN = 2
Y_COLUMN = 1
X_WINDOW_SIZE = 1
Y_WINDOW_SIZE = 0.0001

struct = {
    'windowsize': {
        'x': X_WINDOW_SIZE,
        'y': Y_WINDOW_SIZE,
    },
    'time': {
        'min': None,
        'max': None,
    },
    'value': {
        'min': None,
        'max': None,
    },
    'data': {
    },
}

###############################################################################
####################################################################### helpers

def t2i (t):
    return int((t/X_WINDOW_SIZE)*X_WINDOW_SIZE)

def v2i (v):
    return int((v/Y_WINDOW_SIZE)*Y_WINDOW_SIZE)

def consume (time, value):
    i = t2i(time)
    j = v2i(value)
    
    # update boundaries
    if struct['time']['min']==None or i<struct['time']['min']:
        struct['time']['min'] = i
    if struct['time']['max']==None or i>struct['time']['max']:
        struct['time']['max'] = i
    if struct['value']['min']==None or value<struct['value']['min']:
        struct['value']['min'] = j
    if struct['value']['max']==None or value>struct['value']['max']:
        struct['value']['max'] = j
    print(i,j)
    # increment heatmap index
    if not i in struct['data']: struct['data'][i] = {}
    if not j in struct['data'][i]: struct['data'][i][j] = 0
    struct['data'][i][j] += 1

###############################################################################
########################################################################## main

# guard: command line arguments
if len(argv)!=3:
    print('Syntax: %s CSV_FILENAME JSON_FILENAME' % argv[0])
    print('        %s adct5.log heatmap.json' % argv[0])
    exit(1)
input_filename  = argv[1]
output_filename = argv[2]

# process data
with open(input_filename) as fo:
    i = -1
    print('about to start')
    lasttime  = None
    lastvalue = None
    for line in fo:
        i += 1
        line = line.strip()
        if len(line)==0: continue
        if line[0]=='#': continue
        
        parts = line.split(sep)
        
        if len(parts)!=4:
            print('Error parsing line "%s".' % line)
            continue
        
#        print(i, lasttime, lastvalue)
        value = float(parts[Y_COLUMN])*1000
        time  = int(  parts[X_COLUMN])
        if lasttime!=None and lastvalue!=None:
            if value-lastvalue<1024:
                consume(time-lasttime, value-lastvalue)
        lasttime  = time
        lastvalue = value

struct['time']['max']  += X_WINDOW_SIZE
struct['value']['max'] += Y_WINDOW_SIZE

# write result to disk
with open(output_filename, 'w') as fo:
    fo.writelines([json.dumps(struct)])

