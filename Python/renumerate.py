#!/usr/bin/env python
 
"""
    Create symlinks from a set of paths returned by glob for FFmpeg to read
"""
     
import os
import glob
import time




pfad = os.path.abspath(os.path.curdir)

files = sorted(glob.glob(pfad + "/*.JPG"))
 
outdir = pfad + "/processing02"
 
print outdir 

if not os.path.exists(outdir):
    print "creating {outdir}"
    os.makedirs(outdir)

i = 1
for i, f in enumerate(files):
    print "Linking " + f + " => " + os.path.join(outdir, "%05d.jpg" % (i + 1))
    os.symlink(f, os.path.join(outdir, "%05d.jpg" % (i + 1)))
