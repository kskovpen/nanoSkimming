# Skim nanoAOD files using CRAB

### Introduction
This repository can be used to read remote nanoAOD files via DAS, skim them, and write them to a local storage site. 
The skimming step does not only include selection of interesting events, but also the addition of new variables, so they do not have to be recomputed every time on the fly.

### How to install
This repository is based on [nanoAOD-tools](https://github.com/cms-nanoAOD/nanoAOD-tools/tree/master), so the first step consists in installing that package.
In principle, nanoAOD-tools can be installed independently from CMSSW, but we need an installation within CMSSW here for CRAB submission.
To install nanoAOD-tools in the correct way:

    cd $CMSSW_BASE/src  
    git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools  
    cmsenv  
    scram b

In addition, you need to install the latest Rochester corrections if you want to use these:
```
cd $CMSSW_BASE/src/PhysicsTools/NanoAODTools
cd python/postprocessing/data
# If a Gitlab SSH token is available:
git clone ssh://git@gitlab.cern.ch:7999/akhukhun/roccor.git roccor.Run2.v5
# or using https:
git clone https://gitlab.cern.ch/akhukhun/roccor.git roccor.Run2.v5

cd roccor.Run2.v5
git checkout Run2.v5
```

Next, install this repository in a similar way:

    cd $CMSSW_BASE/src
    git clone https://github.com/GhentAnalysis/nanoSkimming.git PhysicsTools/nanoSkimming  
    cmsenv
    scram b

Finally, make some local changes as discussed in a paragraph below. (Yes, this is not ideal, but a better solution is still to be found.)

### How to use
#### Local testing
For quick local tests, go to the `testing` directory.
The script `testdummy.py` can be used to verify the basic setup, e.g. if nanoAOD-tools can be properly imported.
Run with `python3 testdummy.py -h` to see the available command line options.
The script `testrun.py` contains a slightly more involved workflow, with real-world skim conditions and other processing steps.
Run with `python3 testrun.py -h` to see the available command line options.
Use this for more advanced tests, or write your own test script based on `testrun.py` for more specific tests.
#### CRAB submission
Go to the `crabsubmission` directory.
The main script for CRAB submission is `submit.py`.
Run with `python3 submit.py -h` for a list of available command line options.
This script basically submits the `crabrun.py` script as jobs to CRAB, where `crabrun.py` defines the skimming workflow, similar to `testdummy.py` or `testrun.py`.
Before submission, it is usually a good idea to run `crabrun.py` locally to see if it behaves as expected.
Important: the file `PSet.py` should not normally be modified, with some exceptions mentioned in the comments at the top of the file.
Also the bash script `crabrun.py` should not be modified; it is automatically created by `submit.py` upon submission.
#### Monitoring the progress
Some utility scripts are available to monitor the progress of CRAB jobs.
These scripts are essentially wrappers around the `crab status` command with a more convenient overview of the output. See `crabsubmission/monitoring` and the comments at the top of each script in there.
#### Local submission
The skimming can also be ran locally on HTCondor.
-> under construction
#### Merging
When all CRAB skimming jobs are finished, the resulting samples can be merged into a single file per sample, using the `mergesamples.py` script in the `merging` directory. Run with `python3 mergesamples.py -h` to see a list of available command line options. This script is essentially a wrapper around `haddnano.py` (from NanoAOD-tools). It can be run sequentially/locally as well as in parallel / via HTCondor on the local cluster.

### Making changes
You can write your own nanoAOD-tools modules and add them to the skimming workflow to customize the output. When you do this, there are some things to take into account:
- All modules must derive from the nanoAOD-tools `Module` class, and have the same basic skeleton structure. See the already existing modules (under `python/skimselection` or `python/processing`) for examples, as well as the [nanoAOD-tools](https://github.com/cms-nanoAOD/nanoAOD-tools/tree/master) documentation.
- All modules must be placed in the `python` directory of this repository (or its subdirectories). This is required for `scram` to properly detect them and make them available when using CRAB submission. After writing a new module, rerun `scram b`. After modifying an already existing module, this does not seem to be necessary, but better safe than sorry.
- When you module uses external data (e.g. json files with extra info or ROOT files with weights), these extra files must be placed in the `data` directory of this repository (or its subdirectories). This is needed since this directory will be copied to the working directory in CRAB submission. This also affects the relative path to access these files, which is different when running locally than when using CRAB submission. See `python/processing/triggervariables.py` or `python/processing/topleptonmva.py` for examples of how to deal with this.

### References:
nanoAOD-tools:
- https://github.com/cms-nanoAOD/nanoAOD-tools  

Skimming of nanoAOD files:  
- https://github.com/UBParker/skimNanoAOD/tree/master  
- https://github.com/cms-nanoAOD/nanoAOD-tools/tree/master/crab  

Useful in general: the branch content of nanoAOD files:  
- https://cms-nanoaod-integration.web.cern.ch/autoDoc/  

### Tracking log of changes in third-party source code
- nanoAOD-tools/python/postprocessing/framework/crabhelper.py
  L10,11 commented out, since they appear to be nowhere used
  and mess with custom command line arguments
- CMSSW/bin/haddnano.py
  change shebang from python to python3
- Same change in nanoAOD-tools/scripts/haddnano.py
