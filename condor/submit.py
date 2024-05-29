import glob
import sys
import os
import argparse
from datetime import datetime

import ct_diff as ct


def hascmsenv():
    ### check if cmsenv was set
    target = os.environ['CMSSW_BASE'].replace('/storage_mnt/storage','')
    if target in os.getcwd(): return True
    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Submit skimmer via CRAB')
    parser.add_argument('-s', '--samplelist', required=True, type=os.path.abspath,
                        help='File with dataset names to process -> must be htcondor paths')
    parser.add_argument('-p', '--processor', default='condor/condorrun.py',
                        help='Python script to run on each file')
    parser.add_argument('-o', '--outputdir', default='/pnfs/iihe/cms/store/user/nivanden/nanoaodskims',
                        help='Output directory on /pnfs')
    parser.add_argument('-n', '--nentries', default=-1, type=int,
                        help='Number of entries to process per unit')
    parser.add_argument('-b', '--batchsize', default=10,
                        help='Number of files processed in each job.')
    args = parser.parse_args()

    # fix input/output locations automatically
    # samplelist: pnfs adress basically
    datasets = [dataset.strip() for dataset in open(args.samplelist)]          
    datasets = [dataset.split()[0] for dataset in datasets if dataset and not dataset.startswith('#')] # Clean empty and comment lines
    outputbase = args.outputdir

    dateTimeObj = datetime.now()
    datestring = dateTimeObj.strftime("%Y%m%d_%H%M%S")

    for dataset in datasets:
        # dataset is /pnfs path
        # decide outputdir:
        # first remove trailing / if it exists:
        if dataset[-1] == "/":
            dataset = dataset[:-1]
        # next, generate outputname
        split_dataset = dataset.split("/")[-1] # I think -1, might be -2
        outputdir = os.path.join(outputbase, split_dataset, datestring)
        if not os.path.exists(outputdir):
            os.makedirs(outputdir)

        # in dataset: listdir
        datasetcontent = os.listdir(dataset)
        while os.path.isdir(os.path.join(dataset, datasetcontent[0])):
            dataset = os.path.join(dataset, datasetcontent[0])
            datasetcontent = os.listdir(dataset)

        # make sure they're nano
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
        # print(batched)
        ct.submitCommandsetsAsCondorCluster("SkimNano", batched, scriptfolder="Scripts/condor/")
