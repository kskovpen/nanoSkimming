################################################
# Run nanoSkimming in HTCondor submission mode #
################################################

# Note: run with python3!

# external imports
import glob
import sys
import os
import argparse
from datetime import datetime

# local imports
import condortools as ct


def hascmsenv():
    ### check if cmsenv was set
    target = os.environ['CMSSW_BASE'].replace('/storage_mnt/storage','')
    if target in os.getcwd(): return True
    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Submit skimmer via HTCondor')
    parser.add_argument('-s', '--samplelist', required=True, type=os.path.abspath,
                        help='File with dataset names to process.'
                            +' Note: each dataset must be a locally accessible path (i.e. on /pnfs or your /user).')
    parser.add_argument('-p', '--processor', default='condor/condorrun.py',
                        help='Python script to run on each file (default: condorrun.py in the condor subdirectory).')
    parser.add_argument('-o', '--outputdir', default=f'/pnfs/iihe/cms/store/user/{os.getenv("USER")}/nanoaodskims',
                        help='Output directory (default: <your pnfs space>/nanoaodskims)')
    parser.add_argument('-n', '--nentries', default=-1, type=int,
                        help='Number of entries to process per unit')
    parser.add_argument('-b', '--batchsize', default=50,
                        help='Number of files processed in each job.')
    args = parser.parse_args()

    # read datasets
    datasets = [dataset.strip() for dataset in open(args.samplelist)]          
    datasets = [dataset.split()[0] for dataset in datasets if dataset and not dataset.startswith('#')]
    print('Found following datasets:')
    for d in datasets: print('  - {}'.format(d))

    # set output directory
    outputbase = args.outputdir

    # get current time (for formatting output directory)
    dateTimeObj = datetime.now()
    datestring = dateTimeObj.strftime("%Y%m%d_%H%M%S")

    for dataset in datasets:
        
        # format output directory
        dataset = dataset.rstrip('/')
        split_dataset = dataset.split('/')[-1]
        outputdir = os.path.join(outputbase, split_dataset, datestring)
        if not os.path.exists(outputdir): os.makedirs(outputdir)

        # find all files in the provided dataset directory
        # note: this part is based on a convention where the dataset might
        #       contain an arbitrarily deep chain of subfolders,
        #       but always only one at each level
        #       (until the final depth with the actual root files is reached).
        #       this might need an update in the future, e.g. using os.walk.
        datasetcontent = os.listdir(dataset)
        while os.path.isdir(os.path.join(dataset, datasetcontent[0])):
            dataset = os.path.join(dataset, datasetcontent[0])
            datasetcontent = os.listdir(dataset)

        # make sure they are indeed nanoAOD files
        datasetcontent = glob.glob(os.path.join(dataset, "*NanoAOD*.root"))

        cmds = []
        for file in datasetcontent:
            cmd = "python {}".format(args.processor)
            cmd += " -i {}".format(file)
            cmd += " -n {}".format(args.nentries)
            cmds.append(cmd)

        # add a default command for copying files from tmpdir to outdir
        copy_cmd = "cp $TMPDIR/* {}/".format(outputdir)

        batched = []
        batchsize = args.batchsize
        i=0
        while i * batchsize < len(cmds):
            batch = []
            if ((i+1)* batchsize > len(cmds)):
                batch.extend(cmds[i * batchsize:])
            else:
                batch.extend(cmds[i * batchsize:(i+1) * batchsize])
            batch.append(copy_cmd)
            i += 1
            batched.append(batch)
        ct.submitCommandsetsAsCondorCluster("SkimNano", batched, scriptfolder="Scripts/condor/")
