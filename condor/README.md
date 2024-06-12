# Using condor submission
Using HTCondor for submitting skimming jobs is straightforward.
The workflow is essentially the same as for CRAB submission,
but instead of using `submit.py` in the `crabsubmission` folder, you use the `submit.py` in this folder.

Command line example:
```bash
python3 condor/submit.py -s path/to/samplelist [-p path/to/custom/processor] [-o /path/to/custom/outputfolder] [-n int] [-b int]
```
Where -b is the batchsize, i.e. the number of nanoAOD files processed in each job in the cluster,
and -n is the number of events processed from each file.
Every argument in square brackets is optional.
The default processor is condorrun.py, which should be equivalent to crabrun.py

To do: the duplication of `crabrun.py` into `condorrun.py` might lead to bugs because of unnoticed divergences.
Check if this duplication can be avoided and if a single script can be used instead.
