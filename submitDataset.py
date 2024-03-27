import glob
import sys
import os

import condor.ct_diff as ct

if __name__ == "__main__":
    folder_expr = os.path.join(sys.argv[1], "*.root")
    outputfolder = "/pnfs/iihe/cms/store/user/nivanden/nano_testing/TTTT_EFT/skimmed/"
    files = glob.glob(folder_expr)

    cmds = []
    for file in files:
        cmd = "python testing/run/testrun.py"
        cmd += " -i {}".format(file)
        cmd += " -o {}".format(outputfolder)
    
    batched = []
    batchsize = 10
    i=0
    while i * batchsize < len(cmds):
        batch = []
        if ((i+1)* batchsize > len(cmds)):
            batch.extend(cmds[i * batchsize:])
        else:
            batch.extend(cmds[i * batchsize:(i+1) * batchsize])
        i += 1
        batched.append(batch)

    ct.submitCommandsetsAsCondorCluster("SkimNano", batched, scriptfolder="Scripts/condor/")
