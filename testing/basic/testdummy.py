#!/usr/bin/env python

########################################
# Testing script using a dummy skimmer #
########################################

# imports
import os, sys
import argparse
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True # (?)
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from testskimmer import TestSkimmer

# input arguments:
parser = argparse.ArgumentParser(description='Perform a simple test skim')
parser.add_argument('-i', '--inputfile', required=True, type=os.path.abspath)
parser.add_argument('-o', '--outputdir', required=True, type=os.path.abspath)
parser.add_argument('-n', '--nentries', type=int, default=-1)
parser.add_argument('-d', '--dropbranches', default=None)
args = parser.parse_args()

# print arguments
print('Running with following configuration:')
for arg in vars(args):
    print('  - {}: {}'.format(arg,getattr(args,arg)))

# define a PostProcessor
p = PostProcessor(
  args.outputdir,
  [args.inputfile],
  modules = [TestSkimmer()],
  maxEntries = None if args.nentries < 0 else args.nentries,
  postfix = '-skimmed',
  branchsel = args.dropbranches
)

# run the PostProcessor
p.run()
