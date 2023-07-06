################################################
# Merge skimmed files into one file per sample #
################################################

# This functionality is supposed to be run on the output of a skimming job with CRAB,
# see the crabsubmission folder for more info.
# The input folder for this step is supposed to have the following structure:
# <top input directory>/<sample name>/<request name>/<timestamp>/<counter>/<skimmed files>
# The output will look like this:
# <top output directory>/<merged sample files>
# where there is one merged sample file per <sample name> and <request name>.

# Note: the merging is done using simple haddnano.py; 
# it results in one file per sample / primary dataset and era.
# For merging different primary datasets together,
# another procedure involving removal of duplicate events should be employed
# after running the mergesamples step: see mergedatasets.py.

# import python library classes 
import os
import sys
import fnmatch
import argparse

# import other parts of code
sys.path.append(os.path.abspath('../condor'))
import condortools as ct


def get_sample_directories( input_directory ):
    ### get a list of all skimmed samples in a given input directory
    # depends on the naming convention of CRAB, as follows:
    # <input directory>/<sample name>/<request name>
    # where the request name typically contains year/version info
    # (see crabsubmission/crabconfig.py)
    sample_directories = []
    for samplename in os.listdir(input_directory):
        sample_name_directory = os.path.join(input_directory, samplename)
        for version in os.listdir(sample_name_directory):
            sample_directory = os.path.join(sample_name_directory, version)
            sample_directories.append(sample_directory)
    return sample_directories

def get_files_to_merge( sample_directory, usewildcard=True ):
    ### get a list of all files to merge for a given sample
    # depends on the naming convention of CRAB, as follows:
    # <sample directory>/<timestamp>/<counter>/<actual files>
    mergefiles = []
    timestamps = os.listdir(sample_directory)
    if len(timestamps)!=1:
        msg = 'ERROR: found {} time stamps'.format(len(timestamps))
        msg += ' for sample {}'.format(sample_directory)
        msg += ' (while 1 was expected).'
        raise Exception(msg)
    sample_directory = os.path.join(sample_directory, timestamps[0])
    for counter in sorted(os.listdir(sample_directory)):
        counter_directory = os.path.join(sample_directory, counter)
        if usewildcard:
            mergefiles.append(os.path.join(counter_directory,'*.root'))
        else:
            files = sorted([f for f in os.listdir(counter_directory) if f.endswith('.root')])
            for f in files: mergefiles.append(os.path.join(counter_directory,f))
    return mergefiles

def merged_sample_name( sample_directory ):
    ### construct a suitable merged sample name from an sample directory
    # note: depends on naming convention (see crabsubmission/crabconfig.py)
    sample_directory = sample_directory.strip('/')
    sample_parts = sample_directory.split('/')
    # take the sample name from the next-to-last part and the year from the last part
    sample_name = sample_parts[-2]
    yearid = sample_parts[-1].split('_')[-1]
    return sample_name + '_' + yearid + '.root'

 
if __name__ == '__main__':

  # parse arguments
  parser = argparse.ArgumentParser('Merge samples')
  parser.add_argument('-i', '--inputdir', required=True, type=os.path.abspath)
  parser.add_argument('-o', '--outputdir', required=True, type=os.path.abspath)
  parser.add_argument('-r', '--runmode', default='condor', choices=['condor','local'])
  parser.add_argument('-s', '--searchkey', default=None)
  args = parser.parse_args()

  # print arguments
  print('Running with following configuration:')
  for arg in vars(args):
    print('  - {}: {}'.format(arg,getattr(args,arg)))

  # argument checks and parsing
  if not os.path.exists(args.inputdir):
    raise Exception('ERROR: input directory {} does not exist.'.format(args.inputdir))

  # define the samples to merge
  mergedict = {}
  # loop over all directories in the provided top directory
  for sample_directory in get_sample_directories( args.inputdir ):
    # filter out other files that may be present
    if not os.path.isdir(sample_directory): continue
    # check if this sample should be taken into account
    if args.searchkey is not None:
      if not fnmatch.fnmatch(sample_directory,args.searchkey): continue
    # get the input files
    mfiles = get_files_to_merge(sample_directory, usewildcard=True)
    nmfiles = len(get_files_to_merge(sample_directory, usewildcard=False))
    # make corresponding output file
    outputfile = os.path.join( args.outputdir, merged_sample_name(sample_directory) )
    # check if the same output file was already defined
    if outputfile in mergedict.keys():
        raise Exception('ERROR: output file {} defined multiple times.'.format(outputfile))
    # add to the merging dict
    mergedict[outputfile] = {'dir': sample_directory, 'files': mfiles, 'nfiles': nmfiles}
    # do printouts for testing
    #print(sample_directory)
    #print(mfiles)
    #print(nmfiles)

  # check if found anything
  if len(mergedict)==0:
    print('Found no samples to merge, exiting.')
    sys.exit()

  # print before continuing
  print('Found following tuples to merge:')
  for key, val in sorted(mergedict.items()):
    mdir = val['dir']
    nmfiles = val['nfiles']
    print(' - {} ({} files)'.format(mdir, nmfiles))
    print('  --> {}'.format(key))
  print('(Total: {})'.format(len(mergedict)))
  print('Continue? (y/n)')
  go = input()
  if go!='y': sys.exit()

  # continue with the submission
  for outputfile, val in mergedict.items():
    # make the command
    cmd = 'haddnano.py'
    cmd += ' {}'.format(outputfile)
    for mfile in val['files']: cmd += ' {}'.format(mfile)
    # make output directory if needed
    outputdir = os.path.dirname(outputfile)
    if not os.path.exists(outputdir): os.makedirs(outputdir)
    # run the command
    if args.runmode=='local': os.system(cmd)
    elif args.runmode=='condor':
      ct.submitCommandAsCondorJob('cjob_mergesamples', cmd, cmssw_version='auto')
