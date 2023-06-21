##################################
# A simple looper for testrun.py #
##################################
# Run on test files for all years/eras for data and simulation

import sys
import os

# common settings
nentries = 1000
redirector = 'root://cms-xrd-global.cern.ch//'
outputdir = 'output_test'
dropbranches = '../data/dropbranches/default.txt'
dosim2016pre = False
dosim2016post = False
dosim2017 = False
dosim2018 = True
dodata2016 = False
dodata2017 = False
dodata2018 = True

# initializations
inputfiles = []

if dosim2016pre:
    inputfiles.append('/store/mc/RunIISummer20UL16NanoAODAPVv9/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/NANOAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v2/100000/BB4D6117-4E37-7D4B-BFC8-ADF618AB0FEC.root')
if dosim2016post:
    inputfiles.append('/store/mc/RunIISummer20UL16NanoAODv9/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/NANOAODSIM/106X_mcRun2_asymptotic_v17-v1/130000/3804F011-2434-6B40-A8FD-48D9F9865092.root')
if dosim2017:
    inputfiles.append('/store/mc/RunIISummer20UL17NanoAODv9/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/NANOAODSIM/106X_mc2017_realistic_v9-v1/270000/0D1583EC-5199-934D-81D7-491CB7631105.root')
if dosim2018:
    inputfiles.append('/store/mc/RunIISummer20UL18NanoAODv9/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/70000/31777CCD-9BEE-C54C-8512-9812249A0325.root')

if dodata2016:
    pass # to do

if dodata2017:
    pass # to do

if dodata2018:
    # add input files for 2018 data
    inputfiles.append('/store/data/Run2018A/DoubleMuon/NANOAOD/UL2018_MiniAODv2_NanoAODv9-v1/270000/0B7C8114-450F-734B-8626-732B42EBEEC4.root')
    inputfiles.append('/store/data/Run2018B/DoubleMuon/NANOAOD/UL2018_MiniAODv2_NanoAODv9-v1/270000/26A32EF4-689F-B742-BCA5-60E60FAE1D95.root')
    inputfiles.append('/store/data/Run2018C/DoubleMuon/NANOAOD/UL2018_MiniAODv2_NanoAODv9-v1/130000/18E1280E-04BB-2D44-96D7-AF41AEC73CEA.root')
    inputfiles.append('/store/data/Run2018D/DoubleMuon/NANOAOD/UL2018_MiniAODv2_NanoAODv9-v2/2430000/10B35369-7C64-3640-B0A5-6E12AEDEA06B.root')

# add redirector
inputfiles = [redirector+f for f in inputfiles]

# loop over input files
for f in inputfiles:
    # make the command
    cmd = 'python3 testrun.py'
    cmd += ' -i {}'.format(f)
    cmd += ' -o {}'.format(outputdir)
    cmd += ' -n {}'.format(nentries)
    cmd += ' -d {}'.format(dropbranches)
    # print the command
    print('Will run following command:')
    print(cmd)
    # run the command
    os.system(cmd)
