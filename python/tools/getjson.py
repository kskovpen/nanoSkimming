####################################################################
# Get run and lumisection numbers in a NanoAOD file in json format #
####################################################################

# imports
import sys
import os
import json
import numpy as np
import awkward as ak
import uproot
import argparse


def get_lumis_uproot(rootfile):
  ### get lumisections in a local file using uproot
  rkey = 'run'
  lkey = 'luminosityBlock'
  # open file and read branches
  with uproot.open(inputfile) as f:
    events = f['Events']
    nevents = events.num_entries
    eventids = events.arrays([rkey, lkey], library='np')
    runs = eventids[rkey]
    lumis = eventids[lkey]
  # remove duplicates and bring in correct format
  runsls = {}
  for i in range(nevents):
    run = int(runs[i])
    lumi = int(lumis[i])
    if run not in runsls.keys():
      runsls[run] = [[lumi, lumi]]
    elif lumi != runsls[run][-1][-1]:
      runsls[run].append([lumi, lumi])
  return runsls

def get_lumis_das(dasfile):
  ### get lumisections in a remote file using DAS client
  dascmd = "dasgoclient -query 'lumi file={}' --limit 0".format(dasfile)
  dasstdout = os.popen(dascmd).read()
  lumis = sorted([el.strip(' \t') for el in dasstdout.strip('\n').split('\n')])
  dascmd = "dasgoclient -query 'run file={}' --limit 0".format(dasfile)
  dasstdout = os.popen(dascmd).read()
  runs = sorted([el.strip(' \t') for el in dasstdout.strip('\n').split('\n')])
  if len(runs)!=1:
    msg = 'ERROR: found {} runs ({}), which is unexpected.'.format(len(runs), runs)
    raise Exception(msg)
  run = int(runs[0])
  lumis = sorted([int(el) for el in set(lumis)])
  runsls = {run: []}
  for lumi in lumis: runsls[run].append([lumi,lumi])
  return runsls

def combine_lumis(runsls, mode='union'):
  ### combine sets of json formatted lumisections
  if mode=='union': raise Exception('Not yet implemented')
  elif mode=='intersection':
    totrunsls = {}
    firstrunsls = runsls[0]
    for run in sorted(firstrunsls.keys()):
      keeprun = True
      for otherrunsls in runsls[1:]:
        if run not in otherrunsls.keys(): keeprun = False
      if not keeprun: continue
      for lumi in sorted(firstrunsls[run]):
        keeplumi = True
        for otherrunsls in runsls[1:]:
          if lumi not in otherrunsls[run]: keeplumi = False
        if not keeplumi: continue
        if run in totrunsls.keys(): totrunsls[run].append(lumi)
        else: totrunsls[run] = [lumi]
    return totrunsls
  else: raise Exception('ERROR: mode {} not recognized.'.format(mode))


if __name__=='__main__':

  # input arguments
  parser = argparse.ArgumentParser(description='Get lumis in json format')
  parser.add_argument('-i', '--inputfiles', required=True, nargs='+')
  parser.add_argument('-o', '--outputfile', default=None)
  parser.add_argument('-m', '--mode', default='union', choices=['union','intersection'])
  args = parser.parse_args()

  # print arguments
  print('Running with following configuration:')
  for arg in vars(args):
    print('  - {}: {}'.format(arg,getattr(args,arg)))

  # loop over input files
  runsls = []
  for inputfile in args.inputfiles:
    # find lumisections
    if os.path.exists(inputfile):
      thisrunsls = get_lumis_uproot(inputfile)
    else: thisrunsls = get_lumis_das(inputfile)
    runsls.append(thisrunsls)

  # process into a single list of lumisections
  if len(runsls)>1: runsls = combine_lumis(runsls, mode=args.mode)
  else: runsls = runsls[0]

  # determine number of lumisections
  nls = 0
  for key, val in runsls.items():
    nls += len(val)

  # printouts for testing
  print('Number of runs: {}'.format(len(runsls.keys())))
  print('Number of lumisections: {}'.format(nls))

  # convert to json
  if args.outputfile is not None:
    with open(args.outputfile, 'w') as f:
      json.dump(runsls, f)
