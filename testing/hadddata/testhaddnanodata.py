#!/usr/bin/env python

######################################
# Script for testing haddnanodata.py #
######################################

# imports
import os, sys
from pathlib import Path

# import local tools
sys.path.append(str(Path(__file__).parents[2]))
from merging.haddnanodata import haddnanodata

# read output file to create
output_path = sys.argv[1]

# read input files
input_paths = sys.argv[2:]

# for quicker testing: read only the index branches + a few others
#keep_branches = None
keep_branches = ["event", "run", "luminosityBlock", "nMuon", "nElectron"]

# perform the hadding
haddnanodata(
    output_path,
    input_paths,
    verbose=True,
    keep_branches=keep_branches,
    force=True )
