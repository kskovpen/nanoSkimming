# imports
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True # (?)

# import nanoAODTools
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection,Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


class TestSkimmer(Module):

    def __init__(self):
        ### intializer
        # empty for now
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        ### process a single event
        # return True (go to next module) or False (skip this event)

        # get electrons and muons
        electrons = list(Collection(event, "Electron"))
        muons = list(Collection(event, "Muon"))
        
        # perform dummy selection
        if( len(electrons) + len(muons) < 2 ): return False
        return True
