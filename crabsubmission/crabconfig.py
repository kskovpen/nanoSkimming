###########################
# CRAB configuration file #
###########################
# more info:
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3ConfigurationFile

# imports
import sys
import os

# import CMSSW tools
from WMCore.Configuration import Configuration

# get modifiable parameters from the environment (set by the submit script)
dataset = os.environ['CRAB_DATASET']
outputDir = os.environ['CRAB_OUTPUTDIR']
processor = os.environ['CRAB_PROCESSOR']
script = os.environ['CRAB_SCRIPT']
(_, sample, version, tier) = dataset.split('/')
# (first value is just an empty string because dataset starts with /)
shortsample = sample.split('_')[0]
shortversion = version.split('-')[0]

# define a name and a workarea for this CRAB workflow
requestName = shortsample + '_' + shortversion
workArea = os.path.join(os.environ['CMSSW_BASE'],
             'src/PhysicsTools/nanoSkimming/crabsubmission/crablogs',
             sample, version)

# define an output directory
# note: the first part should always be /store/user/<username>
#       which on T2_BE_IIHE redirects to /pnfs/iihe/cms/store/user/<username>;
#       only the subdirectory can be freely chosen
outLFNDirBase = '/store/user/' + os.environ['USER']
outLFNDirBase = os.path.join(outLFNDirBase, outputDir)

# crab configuration
config = Configuration()
config.section_('General')
config.General.transferLogs            = True
config.General.requestName             = requestName
config.General.workArea                = workArea

config.section_('JobType')
config.JobType.psetName                = 'PSet.py'
config.JobType.scriptExe               = script
config.JobType.inputFiles              = [processor, '../data']
config.JobType.inputFiles.append('../../NanoAODTools/scripts/haddnano.py')
# (note: the above addition might seem to be superfluous,
#  as haddnano.py is added in the CMSSW/bin;
#  however, for a yet unknown reason that seems not to work,
#  and explicitly adding the NanoAODTools script seems to be needed.)
config.JobType.pluginName              = 'Analysis'
config.JobType.outputFiles             = ['skimmed.root']
# (note: this value must correspond to the one in PSet.py and crabrun.py;
#  this argument can in principle also be left out altogether as PSet.py
#  already specifies the output file name.)
config.JobType.sendExternalFolder      = True
config.JobType.sendPythonFolder        = True
config.JobType.allowUndistributedCMSSW = True
config.JobType.numCores                = 1
config.JobType.maxJobRuntimeMin        = 1315 if 'SIM' in dataset else 2630
# (note: default is 1315, which appears to be slightly too short
#  for some data files, so used double runtime limit here)

config.section_('Data')
config.Data.inputDataset               = dataset
config.Data.unitsPerJob                = 1 if 'SIM' in dataset else 1
config.Data.splitting                  = 'FileBased'
# (note: "LumiBased" splitting does not seem to work correctly for NanoAOD data,
#  perhaps because CRAB cannot extract the lumi number from the NanoAOD format)
config.Data.outLFNDirBase              = outLFNDirBase
config.Data.publication                = False
config.Data.lumiMask                   = None
# (note: the golden json selection is implemented at the PostProcessor level,
#  not at the CRAB job level, so the lumiMask can be set to None)
config.Data.allowNonValidInputDataset  = True

config.section_('Site')
config.Site.storageSite                = 'T2_BE_IIHE'
