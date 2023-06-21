#!/usr/bin/env python

#####################################
# Testing script for json selection #
#####################################

# imports
import os, sys
import argparse

# import tools from NanoAODTools
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

# import local tools
from PhysicsTools.nanoSkimming.skimselection.jsonskimmer import JsonSkimmer
from PhysicsTools.nanoSkimming.tools.sampletools import getsampleparams

# input arguments
parser = argparse.ArgumentParser(description='Test')
parser.add_argument('-i', '--inputfile', required=True)
parser.add_argument('-o', '--outputdir', required=True, type=os.path.abspath)
parser.add_argument('-n', '--nentries', type=int, default=-1)
parser.add_argument('-d', '--dropbranches', default=None)
args = parser.parse_args()

# parse input file
if not args.inputfile.startswith('root://'):
    args.inputfile = os.path.abspath(args.inputfile)

# print arguments
print('Running with following configuration:')
for arg in vars(args):
    print('  - {}: {}'.format(arg,getattr(args,arg)))

# get sample parameters
sampleparams = getsampleparams(args.inputfile)
year = sampleparams['year']
dtype = sampleparams['dtype']
print('Sample is found to be {} {}.'.format(year,dtype))

# define json preskim
jsonfile = '../data/lumijsons/lumijson_{}.json'.format(year)

# define modules
modules = ([
  JsonSkimmer(year=year)
])

# set input files
inputfiles = [args.inputfile]

# set other arguments
postfix = '-skimmed'

# define a PostProcessor
p = PostProcessor(
  args.outputdir,
  inputfiles,
  jsonInput = jsonfile,
  modules = modules,
  maxEntries = None if args.nentries < 0 else args.nentries,
  postfix = postfix,
  branchsel = args.dropbranches
)

# run the PostProcessor
p.run()
