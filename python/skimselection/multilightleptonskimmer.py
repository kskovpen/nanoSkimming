#################################################################
# Skimmer class to select events with 2 SS or > 2 light leptons #
#################################################################

# imports
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import sys
import os
from pathlib import Path

# import nanoAODTools
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection,Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

# import local tools
sys.path.append(str(Path(__file__).parents[1]))
from objectselection.electronselection import electronselection
from objectselection.muonselection import muonselection


class MultiLightLeptonSkimmer(Module):

    def __init__( self, 
                  electron_selection_id=None,
                  muon_selection_id=None ):
        ### intializer
        # input arguments:
        # - electron_selection_id: selection identifier for electrons
        #   (see objectselection/electronselection.py)
        # - electron_selection_id: selection identifier for muons
        #   (see objectselection/muonselection.py)
        self.electron_selection_id = electron_selection_id
        self.muon_selection_id = muon_selection_id
        print('Initialized a MultiLightLeptonSkimmer module with following parameters:')
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
        selected_leptons = selected_electrons + selected_muons
        
        # perform event selection
        if( len(selected_leptons) < 2 ): return False
        if( len(selected_leptons) > 2 ): return True
        if( selected_leptons[0].charge == selected_leptons[1].charge ): return True
        return False
