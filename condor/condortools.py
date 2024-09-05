#
# functionality for making job description files for the condor submission system #
#
# documentation:
# - T2B wiki: https://t2bwiki.iihe.ac.be/HTCondor
# - HTCondor manual: https://htcondor.readthedocs.io/en/latest/users-manual/index.html

# general use:
# two ingredients are needed for a condor job:
# - a job description (.txt) file
# - an executable
# the functions in this tool allow creating an executable bash script (similar as for qsub)
# and its submission via a job description file

import os
import sys


def makeUnique(fname, scriptfolder=""):
    # make a file name unique by appending a number to it,
    # e.g. test.txt -> test1.txt (in case test.txt already exists)
    # Next part commented out, for consistency keep names always with numbers
    # if not os.path.exists(fname):
    #     return fname
    [name, ext] = os.path.splitext(fname)
    app = 0
    while app < 2500:
        tryname = name + str(app) + ext
        if not os.path.exists(os.path.join(scriptfolder, tryname)):
            return tryname
        app += 1
    msg = 'ERROR: already 2500 files named {} exist;'.format(fname)
    msg += ' consider choosing more specific names, splitting in folders, etc.'
    raise Exception(msg)


def initJobScript(name, scriptfolder="", cwd=None):
    # initialize an executable bash script by setting correct cms env
    # but copied here to be more standalone
    # parse argument
    name = os.path.splitext(name)[0]
    fname = os.path.join(scriptfolder, name + '.sh')
    if os.path.exists(fname):
        os.system('rm {}'.format(fname))
    if( scriptfolder is not None and scriptfolder!="" and not os.path.exists(scriptfolder) ):
        os.makedirs(scriptfolder)
    if cwd is not None: cwd = os.path.abspath(os.getcwd())
    # write script
    with open(fname, 'w') as script:
        script.write('#!/bin/bash\n')
        script.write(f'cd {os.getenv("CMSSW_BASE")}/src\n')
        script.write('source /cvmfs/cms.cern.ch/cmsset_default.sh\n')
        script.write('eval `scram runtime -sh`\n')
        script.write('export X509_USER_PROXY=/user/$USER/x509up_u$(id -u $USER)\n')
        script.write('cd {}\n'.format(cwd))
        script.write('echo "{}"\n\n'.format(fname))

    os.system('chmod +x ' + fname)
    print('initJobScript created {}'.format(fname))


def makeJobDescription(name, exe,
    argstring=None, stdout=None, stderr=None, log=None,
    cpus=1, mem=1024, disk=10240, jdName=None,
    scriptfolder="", logfolder=""):
    # create a single job description txt file
    # note: exe can for example be a runnable bash script
    # note: argstring is a single string containing the arguments to exe (space-separated)

    # parse arguments:
    name = os.path.splitext(name)[0]
    if jdName: fname = jdName
    else: fname = name + '.sub'

    # remove file with same name if it already exists
    pathToFname = os.path.join(scriptfolder, fname)
    if os.path.exists(pathToFname): os.system('rm {}'.format(pathToFname))

    # set names of out, err and log files
    if stdout is None: stdout = name + '_out_$(ClusterId)_$(ProcId).txt'
    if stderr is None: stderr = name + '_err_$(ClusterId)_$(ProcId).txt'
    if log is None: log = name + '_log_$(ClusterId)_$(ProcId).txt'
    
    # make directory for out, err and log files
    current_dir = os.getcwd()
    if not os.path.exists(os.path.join(current_dir, logfolder)):
        os.makedirs(os.path.join(current_dir, logfolder))

    # make job description file
    with open(pathToFname, 'w') as f:
        f.write('executable = {}\n'.format(os.path.join(scriptfolder, exe)))
        if argstring is not None: f.write('arguments = "{}"\n\n'.format(argstring))
        f.write(f"output = {current_dir}/{logfolder}/{stdout}\n")
        f.write(f"error = {current_dir}/{logfolder}/{stderr}\n")
        f.write(f"log = {current_dir}/{logfolder}/{log}\n\n")
        # f.write('request_cpus = {}\n'.format(cpus)) # don't specify if not necessary
        # f.write('request_memory = {}\n'.format(mem)) # don't specify if not necessary
        # f.write('request_disk = {}\n\n'.format(disk)) # don't specify if not necessary
        # f.write('should_transfer_files = yes\n\n')
        # (not fully sure whether to put 'yes', 'no' or omit it completely)
        # f.write('queue\n\n')
    print('makeJobDescription created {}'.format(pathToFname))


def submitCondorJob(jobDescription, addArgs="", scriptfolder=""):
    # submit a job description file as a condor job
    fname = os.path.join(scriptfolder, os.path.splitext(jobDescription)[0] + '.sub')
    if not os.path.exists(fname):
        msg = 'ERROR: job description file {} not found'.format(fname)
        raise Exception(msg)
    # maybe later extend this part to account for failed submissions etc!
    os.system('condor_submit {} {}'.format(fname, addArgs))


def submitCommandAsCondorJob(name, command,
    stdout=None, stderr=None, log=None,
    cpus=1, mem=1024, disk=10240,
    scriptfolder="", logfolder=""):
    # submit a single command as a single job
    # command is a string representing a single command (executable + args)
    submitCommandsAsCondorJobs(name, [[command]],
                               stdout=stdout, stderr=stderr, log=log,
                               cpus=cpus, mem=mem, disk=disk,
                               scriptfolder=scriptfolder, logfolder=logfolder)


def submitCommandsAsCondorCluster(name, commands,
    stdout=None, stderr=None, log=None,
    cpus=1, mem=1024, disk=10240,
    scriptfolder="", logfolder=""):
    # run several similar commands within a single cluster of jobs
    # note: each command must have the same executable and number of args, only args can differ!
    # note: commands can be a list of commands (-> a job will be submitted for each command)
    # parse arguments
    name = os.path.splitext(name)[0]
    shname = makeUnique(name + '.sh')
    jdname = makeUnique(name + '.sub')
    [exe,argstring] = commands[0].split(' ',1) # exe must be the same for all commands
    nargs = len(argstring.split(' ')) # nargs must be the same for all commands
    # first make the executable
    initJobScript(shname, scriptfolder=scriptfolder)
    with open(os.path.join(scriptfolder, shname), 'a') as script:
        script.write(exe)
        # for i in range(nargs): script.write(' ${}'.format(i+1))
        script.write(' $@')
        script.write('\n')
    # then make the job description
    # first job:
    makeJobDescription(name, shname,
      argstring=argstring, stdout=stdout, stderr=stderr, log=log,
      cpus=cpus, mem=mem, disk=disk, jdName=jdname,
      scriptfolder=scriptfolder, logfolder=logfolder)
    # add other jobs:
    with open(jdname, 'a') as script:
        for command in commands[1:]:
            [thisexe, thisargstring] = command.split(' ', 1)
            thisnargs = len(thisargstring.split(' '))
            if (thisexe != exe or thisnargs != nargs):
                msg = 'ERROR: commands are not compatible to put in same cluster'
                raise Exception(msg)
            script.write('arguments = "{}"\n'.format(thisargstring))
            script.write('queue\n\n')
    # finally submit the job
    submitCondorJob(jdname)


def submitCommandsAsCondorJob(name, commands, stdout=None, stderr=None, log=None,
                              cpus=1, mem=1024, disk=10240,
                              scriptfolder="", logfolder=""):
    # submit a set of commands as a single job
    # commands is a list of strings, each string represents a single command (executable + args)
    # the commands can be anything and are not necessarily same executable or same number of args.
    submitCommandsAsCondorJobs(name, [commands], stdout=stdout, stderr=stderr, log=log,
                               cpus=cpus, mem=mem, disk=disk,
                               scriptfolder=scriptfolder, logfolder=logfolder)


def submitCommandsAsCondorJobs(name, commands, stdout=None, stderr=None, log=None,
                               cpus=1, mem=1024, disk=10240,
                               scriptfolder="", logfolder=""):
    # submit multiple sets of commands as jobs (one job per set)
    # commands is a list of lists of strings, each string represents a single command
    # the commands can be anything and are not necessarily same executable or number of args.
    for commandset in commands:
        # parse arguments
        name = os.path.splitext(name)[0]
        shname = makeUnique(name + '.sh', scriptfolder=scriptfolder)
        jdname = makeUnique(name + '.sub', scriptfolder=scriptfolder)
        # first make the executable
        initJobScript(shname, scriptfolder=scriptfolder)
        with open(os.path.join(scriptfolder, shname), 'a') as script:
            for cmd in commandset:
                script.write(cmd + '\n')
        # then make the job description
        makeJobDescription(name,shname,stdout=stdout,stderr=stderr,log=log,
                           cpus=cpus,mem=mem,disk=disk,jdName=jdname,
                           scriptfolder=scriptfolder, logfolder=logfolder)
        with open(os.path.join(scriptfolder, jdname), 'a') as jdScript:
            jdScript.write('queue\n\n')

        # finally submit the job
        submitCondorJob(jdname, addArgs='-batch-name "{}"'.format(name), scriptfolder=scriptfolder)


def submitCommandsetsAsCondorCluster(name, commands, 
    stdout=None, stderr=None, log=None,
    cpus=1, mem=1024, disk=10240,
    scriptfolder="", logfolder="", cwd=None):
    # submit multiple sets of commands as one cluster (one job of the cluster per set)
    # commands is a list of lists of strings, each string represents a single command
    # the commands can be anything and are not necessarily same executable or number of args.
    # parse arguments
    name = os.path.splitext(name)[0]
    shname = makeUnique(name + '.sh', scriptfolder)
    jdname = makeUnique(name + '.sub', scriptfolder)
    # first make the executable
    initJobScript(shname, scriptfolder=scriptfolder, cwd=cwd)
    with open(os.path.join(scriptfolder, shname), 'a') as script:
        for i, commandset in enumerate(commands):
            script.write(f"if [ $1 -eq {i} ]; then\n")
            for cmd in commandset:
                script.write("  " + cmd + '\n')
            script.write("fi\n")

    # then make the job description
    # first job:
    makeJobDescription(name, shname, stdout=stdout, stderr=stderr, log=log,
                       cpus=cpus, mem=mem, disk=disk, jdName=jdname,
                       scriptfolder=scriptfolder, logfolder=logfolder)

    with open(os.path.join(scriptfolder, jdname), 'a') as jdScript:
        jdScript.write("arguments = $(ProcId)\n")
        jdScript.write(f'queue {len(commands)}\n\n')

    # finally submit the job
    submitCondorJob(jdname, addArgs='-batch-name "{}"'.format(name), scriptfolder=scriptfolder)


def submitScriptAsCondorJob(scriptName):
    jdName = os.path.splitext(scriptName)[0]
    makeJobDescription(scriptName, scriptName)
    submitCondorJob(scriptName)
