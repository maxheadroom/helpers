#!/bin/bash
#
# make a snapshot of paper or whiteboard more readable
# by focus on the drawing instead of background/paper


convert $1 -morphology Convolve DoG:15,100,0 -negate -normalize -blur 0x1 -channel RBG -level "60%,91%,0.1" $2
