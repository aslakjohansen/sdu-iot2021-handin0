#!/usr/bin/env python3
# Aslak Johansen <aslakj@gmail.com>

from sys import argv, exit
import json
import cairo
from math import pi

# convenient conversion functions
def inch (i): return float(i)*72.0
def mm (mm): return inch(float(mm)/25.4)

# inputs
w = mm(160)
h = mm(100)
yscale_width = mm(15)
WEST_OFFSET = mm(5)

style = {
    'framewidth':    mm(0.25),
    'textsize':      10.0,
    'titletextsize': 12.0,
    'border':        mm(2),
    'markdia':       mm(1),
    'ticksize':      mm(1),
}

###############################################################################
##################################################################### renderers

def render_init ():
    global ct
    surface = cairo.PDFSurface(output_filename, w, h)
    ct = cairo.Context(surface)
    ct.select_font_face("LMRoman10", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ct.set_font_size(style['textsize'])

def render_title (title):
    ct.save()
    ct.set_font_size(style['titletextsize'])
    x_bearing, y_bearing, textwidth, textheight = ct.text_extents(title)[:4]
    x = west+(east-west)/2 - (x_bearing+textwidth)/2
    ct.move_to(x, style['border']+style['titletextsize'])
    ct.show_text(title)
    ct.restore()

def render_heatmap ():
    # find max count
    cmax = 0
    for time in struct['data']:
        for value in struct['data'][time]:
            if struct['data'][time][value]>cmax: cmax = struct['data'][time][value]
    print('max_count=', cmax)
    
    # fill background
    ct.save()
    ct.move_to(west, north)
    ct.line_to(west, south)
    ct.line_to(east, south)
    ct.line_to(east, north)
    ct.close_path()
    ct.set_source_rgba(1.0, 0.0, 0.0, 0.2)
    ct.fill()
    ct.restore()
    
    # fill tiles
    for time in struct['data']:
        for value in struct['data'][time]:
            t = float(time)
            v = int(value)
            count = struct['data'][time][value]
            rcount = float(count)/cmax
            ct.save()
            ct.move_to(xscale(t), yscale(v))
            ct.line_to(xscale(t), yscale(v+1))
            ct.line_to(xscale(t+X_WINDOW_SIZE), yscale(v+1))
            ct.line_to(xscale(t+X_WINDOW_SIZE), yscale(v))
            ct.close_path()
            ct.set_source_rgb(1.0-rcount, 1.0-rcount, 1.0)
            ct.fill()
            ct.restore()

def render_xaxis (label, unit, minorstep, majorstep, labeler):
    t = 0
    
    while t+tmin<=tmax:
        major = t % majorstep==0
        x = xscale(t+tmin)
        
        # line
        ct.save()
        ct.set_line_width(style['framewidth']*(1 if major else 0.5))
        ct.move_to(x, north)
        ct.line_to(x, south+style['ticksize'])
        ct.set_source_rgba(0.0, 0.0, 0.0, 0.2)
        ct.stroke()
        ct.restore()
        
        # tick text
        if major:
            thuman = labeler(t)
            x_bearing, y_bearing, textwidth, textheight = ct.text_extents(thuman)[:4]
            x -= (x_bearing+textwidth)/2
            
            ct.save()
            ct.move_to(x, south+(style['border']+style['textsize']))
            ct.show_text(thuman)
            ct.restore()
        
        t += minorstep
    
    # label
    text = '%s / [%s]' % (label, unit)
    x_bearing, y_bearing, textwidth, textheight = ct.text_extents(text)[:4]
    x = west+(east-west)/2 - (x_bearing+textwidth)/2
    ct.save()
    ct.set_font_size(style['textsize'])
    ct.move_to(x, south+2*(style['border']+style['textsize']))
    ct.show_text(text)
    ct.restore()

def render_yaxis (label, unit, minorstep, majorstep, labeler):
    v = ((vmin+1)//majorstep)*majorstep
    
    while v<=vmax:
        major = v % majorstep==0
        y = yscale(v)
        
        if y>south:
            v += 1 # TODO: move to start
            continue
        
        # line
        ct.save()
        ct.set_line_width(style['framewidth']*(1 if major else 0.5))
        ct.move_to(west-style['ticksize'], y)
        ct.line_to(east                  , y)
        ct.set_source_rgba(0.0, 0.0, 0.0, 0.2)
        ct.stroke()
        ct.restore()
        
        # tick text
        if major:
            vhuman = labeler(v)
            x_bearing, y_bearing, textwidth, textheight = ct.text_extents(vhuman)[:4]
            x = west-(style['border']+x_bearing+textwidth)
            
            ct.save()
            ct.move_to(x, y+style['textsize']/3)
            ct.show_text(vhuman)
            ct.restore()
        
        v += minorstep
    
    # label
    text = '%s / [%s]' % (label, unit)
    x_bearing, y_bearing, textwidth, textheight = ct.text_extents(text)[:4]
    y = north+(south-north)/2 + (x_bearing+textwidth)/2
    ct.save()
    ct.set_font_size(style['textsize'])
    ct.move_to(style['border']+style['textsize'], y)
    ct.rotate(-pi/2)
    ct.show_text(text)
    ct.restore()

def render_frame ():
    ct.save()
    ct.set_line_width(style['framewidth'])
    ct.move_to(west, north)
    ct.line_to(east, north)
    ct.line_to(east, south)
    ct.line_to(west, south)
    ct.close_path()
    ct.set_source_rgb(0.0, 0.0, 0.0)
    ct.stroke()
    ct.restore()

###############################################################################
########################################################################## plot

def plot_heatmap():
    global east, west, north, south
    global tmin, tmax, vmin, vmax
    global xscale, yscale
    
    # define offsets
    east = w-style['border']
    west = 3*style['border']+style['textsize']+WEST_OFFSET
    north = style['border']+style['titletextsize']+style['border']
    south = h-(3*style['border']+2*style['textsize'])
    
    # define scalers
    tmin = 0 # struct['time']['min']
    tmax = struct['time']['max']
    vmin = 0 # struct['value']['min']
    vmax = struct['value']['max']
#    vmax = 2048
    xscale = lambda t: west +(t-tmin)/(tmax-tmin)*(east-west)
    yscale = lambda v: south-(v-vmin)/(vmax-vmin)*(south-north)
    print(west, east, north, south)
    print(tmin, tmax)
    print(vmin, vmax)
    
    # calculate number of repetitions
    s = 0
    for time in struct['data']:
        for value in struct['data'][time]:
            s += struct['data'][time][value]
    
    render_init()
    render_title('Measured Sampling Period (%d repetitions)' % s)
    render_heatmap()
    render_xaxis('Time Measured on Device'        , 'ms', 1, 10, lambda v: '%d' % v)
    render_yaxis('Time Measured on Laptop', 'ms', 1, 10, lambda v: '%d' % v)
    render_frame()

###############################################################################
########################################################################## main

# guard: command line arguments
if len(argv)!=3:
    print('Syntax: %s JSON_FILENAME PDF_FILENAME' % argv[0])
    print('        %s heatmap.json heatmap.pdf' % argv[0])
    exit(1)
input_filename  = argv[1]
output_filename = argv[2]

# read input
with open(input_filename) as fo:
    struct = json.loads(''.join(fo.readlines()))
X_WINDOW_SIZE = struct['windowsize']['x']
Y_WINDOW_SIZE = struct['windowsize']['y']

plot_heatmap()

