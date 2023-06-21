#################################################
# Skimmer class to select events in a json file #
#################################################
# WARNING: not yet thoroughly tested, nor recommended to be used;
# instead, use the jsonInput argument of the NanoAODTools PostProcessor.

# imports
import sys
import os
import json

# import nanoAODTools
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection,Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


class JsonSkimmer(Module):

    def __init__( self, jsonfile=None, year=None ):
        ### intializer
        # input arguments:
        # - jsonfile: path to json file with run/lumisection selection
        # - year: data taking year, used to find the correct golden json file
        # note: you must specify jsonfile or year, but not both.
        if( jsonfile is None and year is None ):
            raise Exception('ERROR: either jsonfile or year must be specified.')
        if( jsonfile is not None and year is not None ):
            raise Exception('ERROR: you cannot specify both jsonfile and year.')
        if jsonfile is None:
            basename = 'lumijson_{}.json'.format(year)
            jsonfile = os.path.join(os.path.dirname(__file__), '../../data/lumijsons', basename)
            if not os.path.exists(jsonfile):
                # for CRAB submission, the data directory is copied to the working directory
                jsonfile = os.path.join('data/lumijsons', basename)
            if not os.path.exists(jsonfile):
                raise Exception('ERROR: json file {} not found.'.format(jsonfile))
        with open(jsonfile) as f:
            self.json = json.load(f)
        print('Initialized an JsonSkimmer module with following parameters:')
        print('  - json file: {}'.format(jsonfile))

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        ### process a single event
        # return True (go to next module) or False (skip this event)

        # get run and lumisection
        run = event.run
        runstr = str(run)
        lumi = event.luminosityBlock

        # check if they are in the json file
        if not runstr in self.json.keys(): return False
        lumiranges = self.json[runstr]
        for lumirange in lumiranges:
            if( lumirange[0]<=lumi and lumirange[1]>=lumi ): return True
        return False
