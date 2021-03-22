#!/usr/bin/env python3

from sys import argv, exit

# guard: args
if len(argv)!=3:
    print('Syntax: %s INPUT_FILENAME OUTPUT_FILENAME' % argv[0])
    print('        %s t.log t_processed.log' % argv[0])
    exit(1)
input_filename  = argv[1]
output_filename = argv[2]

with open(input_filename) as fo:
    lines = fo.readlines()

output = []
for line in lines:
    elements = line.strip().split(',')
    count = float(elements[2].split(' ')[0])
    time  = float(elements[2].split(' ')[-2])
    output.append('%f,%f,%f\n' % (count, time, time*1000*1000/count))

with open(output_filename, 'w') as fo:
    fo.writelines(output)

