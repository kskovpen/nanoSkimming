################################################################
# Skimmer class to select events with at least n light leptons #
################################################################

# imports
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import sys
import os

# import nanoAODTools
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection,Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

# import local tools
from PhysicsTools.nanoSkimming.objectselection.electronselection import electronselection
from PhysicsTools.nanoSkimming.objectselection.muonselection import muonselection
import PhysicsTools.nanoSkimming.tools.printtools as printtools


class nLightLeptonSkimmer(Module):

    def __init__( self, n, 
                  electron_selection_id=None,
                  muon_selection_id=None ):
        ### intializer
        # input arguments:
        # - n: select events with >= n light leptons
        # - electron_selection_id: selection identifier for electrons
        #   (see objectselection/electronselection.py)
        # - electron_selection_id: selection identifier for muons
        #   (see objectselection/muonselection.py)
        self.n = n
        self.electron_selection_id = electron_selection_id
        self.muon_selection_id = muon_selection_id
        print('Initialized an nLightLeptonSkimmer module with following parameters:')
        print('  - number of leptons threshold: {}'.format(self.n))
        print('  - electron selection ID: {}'.format(self.electron_selection_id))
        print('  - muon selection ID: {}'.format(self.muon_selection_id))

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        ### process a single event
        # return True (go to next module) or False (skip this event)

        # get electrons and muons
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")

        # perform object selection
        selected_electrons = ([el for el in electrons 
          if electronselection(el, self.electron_selection_id)])
        selected_muons = ([mu for mu in muons 
          if muonselection(mu, self.muon_selection_id)])
        
        # perform event selection
        if( len(selected_electrons) + len(selected_muons) < self.n ): return False
        return True
