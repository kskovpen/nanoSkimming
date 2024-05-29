#########################################################################
# Module to add sum of PSWeights as a tree to nanoAOD                   #
#########################################################################

# imports
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import sys
import os
# from pathlib import Path

# import nanoAODTools
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection,Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


class PSWeightSumModule(Module):
    def __init__(self):
        print('Initialized a PSWeightSumModule with following parameters:')

        self.values = [0., 0., 0., 0.]
        return
    
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        # make a new histogram
        self.h_psweightsum = ROOT.TH1D("PSWeightSum", "PSWeightSum", 4, -0.5, 3.5)
        self.genWeight = inputTree.valueReader("genWeight")
        self.PSWeight = inputTree.arrayReader("PSWeight")
        self._ttreereaderversion = inputTree._ttreereaderversion


    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        prevdir = ROOT.gDirectory
        outputFile.cd()
        self.h_psweightsum.Write()
        prevdir.cd()

    def analyze(self, event):
        # process a single event
        # always return true
        # Get PS Weights:
        # print("Event start")
        if event._tree._ttreereaderversion > self._ttreereaderversion:
            self.genWeight = event._tree.valueReader("genWeight")
            self.PSWeight = event._tree.arrayReader("PSWeight")

        # TODO: error handling
        # print(self.PSWeight[0])
        # print(self.PSWeight[1])
        # print(self.PSWeight[2])
        # print(self.PSWeight[3])
        genweight = event.genWeight
        # print(genweight)
        # check if nPSWeight is not 0
        # check if len(PSWeight) == nPSWeight
        

        # for weight in weight: sum
        # end result: Sum of genEventWeight * PSWeight[i] -> so also get the genWeight
        # need to add a fill here!
        for i in range(4):
            # print(self.PSWeight[i])
            totalweight = self.PSWeight[i] * genweight
            # print(totalweight)
            self.h_psweightsum.Fill(i, totalweight)
        # print("Event done")
        return True
