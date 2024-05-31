#Using condor submission
Using the condor submission is very straight forward. You create a samplelist as usual, but instead of using submit.py in crabsubmission, you use the submit.py in this folder.

Command line example:
```bash
python3 condor/submit.py -s path/to/samplelist [-p path/to/custom/processor] [-o /path/to/custom/outputfolder] [-n int] [-b int]
```
Where -b are the batchsize, ie the number of nano files processed in each job in the cluster, and -n the number of events processed from each file. Every argument in square brackets is optional. The default processor is condorrun.py, but should be equivalent to crabrun.py

Next version should harmonize both maybe, oh well