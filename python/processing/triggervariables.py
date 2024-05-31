########################################################################
# Module to add some composite trigger decisons as a branch to nanoAOD #
########################################################################

# imports
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import sys
import os
import json

# import nanoAODTools
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection,Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


class TriggerVariablesModule(Module):

    def __init__(self, year):
        ### intializer
        # path to json file is hard-coded for now, maybe later use an argument.
        triggerdir = os.path.join(os.path.dirname(__file__),'../../data/triggerdefs')
        if not os.path.exists(triggerdir):
            # for CRAB submission, the data directory is copied to the working directory
            triggerdir = 'data/triggerdefs'
        if not os.path.exists(triggerdir):
            raise Exception('ERROR: trigger definition directory not found.')
        triggerfile = os.path.join(triggerdir,'triggerdefs.json')
        with open(triggerfile) as f:
            triggerdefs = json.load(f)
        self.triggerdefs = triggerdefs[year]
        self.triggers = self.triggerdefs.keys()
        print('Initialized a TriggerVariablesModule with following parameters:')
        print('  - year: {}'.format(year))
        print('  - triggers: {}'.format(self.triggers))

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        # find available branches in input file
        branchnames = [str(b.GetName()) for b in inputTree.GetListOfBranches()]
        # loop over composite triggers
        for trigger, hlts in self.triggerdefs.items():
            # the elements in hlts are either a string (a single, required trigger path)
            # or a list (of optional trigger paths)
            required_hlts = [hlt for hlt in hlts if (isinstance(hlt,str) or isinstance(hlt, unicode))]
            optional_hlts = [hlt for hlt in hlts if isinstance(hlt, list)]
            available_hlts = required_hlts[:] # will be appended with available optional triggers

            # check required triggers
            for hlt in required_hlts:
                branchname = 'HLT_{}'.format(hlt)
                if branchname not in branchnames:
                    raise Exception('ERROR: input tree has no branch named {}'.format(branchname))
            # check optional triggers
            for hltlist in optional_hlts:
                for hlt in hltlist:
                    branchname = 'HLT_{}'.format(hlt)
                    if branchname in branchnames:
                        available_hlts.append(hlt)
                    else:
                        msg = 'WARNING: input tree has no branch named {}'.format(branchname)
                        msg += ' but this trigger was marked as optional, so will continue without.'
                        print(msg)
            # set available triggers
            self.triggerdefs[trigger] = available_hlts
            # make output branch
            self.out.branch('HLT_{}'.format(trigger), "O")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        ### process a single event
        # (always return True as this module performs no selection)

        # loop over triggers
        for trigger, hlts in self.triggerdefs.items():
            hltbits = [getattr(event,'HLT_{}'.format(hlt)) for hlt in hlts]
            triggerbit = any(hltbits)
            self.out.fillBranch('HLT_{}'.format(trigger), triggerbit)

        return True
