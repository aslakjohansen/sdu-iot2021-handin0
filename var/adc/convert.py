#!/usr/bin/env python3

from sys import argv, exit

# guard: args
if len(argv)!=3:
    print('Syntax: %s INPUT_FILENAME OUTPUT_FILENAME' % argv[0])
    print('        %s adc.log adc_diff.log' % argv[0])
    exit(1)
input_filename  = argv[1]
output_filename = argv[2]

with open(input_filename) as fo:
    lines = fo.readlines()

output = []
for i in range(len(lines)-1):
    l1 = lines[i].strip().split(',')
    l2 = lines[i+1].strip().split(',')
    output.append('%s,%f,%s\n' % (l2[0], float(l2[0])-float(l1[0]), l2[2]))

with open(output_filename, 'w') as fo:
    fo.writelines(output)

