#!/usr/bin/env python

##########################################
# Testing script using the full workflow #
##########################################

# imports
import os, sys
sys.path.append("../../")
#from data.lumijsons.lumijsons import getlumijson
import argparse
import ROOT
# from pathlib import Path
ROOT.PyConfig.IgnoreCommandLineOptions = True # (?)

# import tools from NanoAODTools
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

# import local tools
# sys.path.append("../../")
from PhysicsTools.nanoSkimming.skimselection.multilightleptonskimmer import MultiLightLeptonSkimmer
from PhysicsTools.nanoSkimming.skimselection.nlightleptonskimmer import nLightLeptonSkimmer
from PhysicsTools.nanoSkimming.processing.leptonvariables import LeptonVariablesModule
from PhysicsTools.nanoSkimming.processing.topleptonmva import TopLeptonMvaModule
from PhysicsTools.nanoSkimming.processing.leptongenvariables import LeptonGenVariablesModule
from PhysicsTools.nanoSkimming.processing.triggervariables import TriggerVariablesModule
from PhysicsTools.nanoSkimming.tools.sampletools import getsampleparams
import PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 as jme

# input arguments
parser = argparse.ArgumentParser(description='Test')
parser.add_argument('-i', '--inputfile', required=True)
parser.add_argument('-o', '--outputdir', required=True, type=os.path.abspath)
parser.add_argument('-n', '--nentries', type=int, default=-1)
parser.add_argument('-d', '--dropbranches', default=None)
parser.add_argument('-j', '--json', default=None)
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

yeardict = {
  '2016PreVFP': 'UL2016_preVFP',
  '2016PostVFP': 'UL2016',
  '2017': 'UL2017',
  '2018': 'UL2018'
}

JetMetCorrector = jme.createJMECorrector(
  isMC=(dtype=='sim'),
  dataYear=yeardict[year],
  jesUncert="Merged",
  splitJER=False
)

# define modules
modules = ([
  nLightLeptonSkimmer(2,
      electron_selection_id='run2ul_loose',
      muon_selection_id='run2ul_loose'),
  LeptonVariablesModule(),
  TopLeptonMvaModule(year, 'ULv1'),
  TriggerVariablesModule(year),
  JetMetCorrector()
])
#if dtype!='data': modules.append(LeptonGenVariablesModule())

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
  jsonInput = args.json
)

# run the PostProcessor
p.run()
