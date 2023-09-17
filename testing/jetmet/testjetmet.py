#!/usr/bin/env python

####################################
# Testing script for JetMET module #
####################################
# More info:
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/NanoAODTools#JME_jetmet_HelperRun2

# imports
import os, sys
import argparse
import ROOT
from pathlib import Path
ROOT.PyConfig.IgnoreCommandLineOptions = True # (?)

# import tools from NanoAODTools
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
import PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 as jme

# import local tools
sys.path.append(str(Path(__file__).parents[2]))
from data.lumijsons.lumijsons import getlumijson
from PhysicsTools.nanoSkimming.skimselection.multilightleptonskimmer import MultiLightLeptonSkimmer
from PhysicsTools.nanoSkimming.skimselection.nlightleptonskimmer import nLightLeptonSkimmer
from PhysicsTools.nanoSkimming.processing.leptonvariables import LeptonVariablesModule
from PhysicsTools.nanoSkimming.processing.topleptonmva import TopLeptonMvaModule
from PhysicsTools.nanoSkimming.processing.leptongenvariables import LeptonGenVariablesModule
from PhysicsTools.nanoSkimming.processing.triggervariables import TriggerVariablesModule
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

# make JetMET module
yeardict = {
  '2016PreVFP': 'UL2016_preVFP',
  '2016PostVFP': 'UL2016',
  '2017': 'UL2017',
  '2018': 'UL2018'
}
jetmetCorrector = jme.createJMECorrector(
  isMC=(dtype=='sim'),
  dataYear=yeardict[year],
  jesUncert="Merged",
  splitJER=True
) 

# define modules
modules = ([
  jetmetCorrector()
])

# set input files
inputfiles = [args.inputfile]

# set other arguments
postfix = '-skimmed'

# define a PostProcessor
p = PostProcessor(
  args.outputdir,
  inputfiles,
  modules = modules,
  maxEntries = None if args.nentries < 0 else args.nentries,
  postfix = postfix,
  branchsel = args.dropbranches,
)

# run the PostProcessor
p.run()
