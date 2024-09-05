###############################################
# Merge datasets with duplicate event removal #
###############################################

# The input folder for this step is supposed to have the following structure:
# <top input directory>/<merged sample files>
# The input directory can hold both simulated and data samples;
# only data samples will be selected for this merging step,
# using the function getsampleparams (see tools/sampletools.py).
# The output will look like this:
# <top output directory>/<merged data samples>
# where there is one merged data file per era.

# Note: this step can take an unreasonably long time to run.
# If possible, it may be best to avoid merging datasets at this level,
# and rather do it after subsequent analysis steps, which much less events remaining.

# import python library classes 
import os
import sys
import fnmatch
import argparse

# import other parts of code
sys.path.append(os.path.abspath('../condor'))
import condortools as ct
from PhysicsTools.nanoSkimming.tools.sampletools import getsampleparams


if __name__ == '__main__':

  # parse arguments
  parser = argparse.ArgumentParser('Merge primary datasets')
  parser.add_argument('-i', '--inputdir', required=True, type=os.path.abspath)
  parser.add_argument('-o', '--outputdir', required=True, type=os.path.abspath)
  parser.add_argument('-n', '--name', default='Data')
  parser.add_argument('-r', '--runmode', default='condor', choices=['condor','local'])
  args = parser.parse_args()

  # print arguments
  print('Running with following configuration:')
  for arg in vars(args):
    print('  - {}: {}'.format(arg,getattr(args,arg)))

  # argument checks and parsing
  if not os.path.exists(args.inputdir):
    raise Exception('ERROR: input directory {} does not exist.'.format(args.inputdir))

  # find data files in input directory
  datafiles = [f for f in os.listdir(args.inputdir) if f.endswith('.root')]
  datafiles = [f for f in datafiles if getsampleparams(f)['dtype']=='data']
  print('Found following data files in input directory:')
  print(datafiles)

  # find available eras
  eras = set([f.split('_')[1].replace('.root','') for f in datafiles])
  print('Found following eras:')
  print(eras)

  # define files to merge per era
  mergedict = {}
  for era in eras:
    inputfiles = [os.path.join(args.outputdir,f) for f in datafiles if era in f]
    outputfile = os.path.join(args.outputdir,args.name + '_' + era + '.root')
    mergedict[outputfile] = inputfiles
  
  # check if found anything
  if len(mergedict)==0:
    print('Found no samples to merge, exiting.')
    sys.exit()

  # print before continuing
  print('Found following tuples to merge:')
  for outputfile, inputfiles in sorted(mergedict.items()):
    for f in inputfiles: print(' - {}'.format(f))
    print('  --> {}'.format(outputfile))
  print('Continue? (y/n)')
  go = input()
  if go!='y': sys.exit()

  # continue with the submission
  for outputfile, inputfiles in sorted(mergedict.items()):
    # make the command
    cmd = 'python3 haddnanodata.py'
    cmd += ' -o {}'.format(outputfile)
    cmd += ' -i'
    for f in inputfiles: cmd += ' {}'.format(f)
    cmd += ' -v -f'
    #cmd += ' --test' # only for testing
    # make output directory if needed
    outputdir = os.path.dirname(outputfile)
    if not os.path.exists(outputdir): os.makedirs(outputdir)
    # run the command
    if args.runmode=='local': os.system(cmd)
    elif args.runmode=='condor':
      ct.submitCommandAsCondorJob('cjob_mergedatasets', cmd,
          scriptfolder='condor_scripts', logfolder='condor_logs')
