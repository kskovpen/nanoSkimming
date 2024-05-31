############################################################################
# Module to add some lepton variables with gen info as a branch to nanoAOD #
############################################################################

# imports
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import sys
import os
# from pathlib import Path

# import nanoAODTools
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection,Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


class LeptonGenVariablesModule(Module):

    def __init__( self, variables=['all'] ):
        ### intializer
        # input arguments:
        # - variables: list of variables names to add
        #   (default: add all variables defined here)
        self.variables = variables
        self.defined_variables = ['isPrompt', 'matchPdgId', 'isChargeFlip', 'provenanceConversion', 'motherPdgId']
        if 'all' in self.variables:
            self.variables = self.defined_variables
        # check provided variables
        for variable in self.variables:
            if variable not in self.defined_variables:
                msg = 'ERROR in LeptonGenVariablesModule:'
                msg += ' variable {} not recognized; options are {}'.format(
                       variable, self.defined_variables)
                raise Exception(msg)
        print('Initialized a LeptonGenVariablesModule with following parameters:')
        print('  - variables:')
        for var in self.variables: print('    - {}'.format(var))

        # define a map of gen particle status codes
        self.statusmap = ({
              'isPrompt': 0,
              'isDecayedLeptonHadron': 1,
              'isTauDecayProduct': 2,  
              'isPromptTauDecayProduct': 3,  
              'isDirectTauDecayProduct': 4,  
              'isDirectPromptTauDecayProduct': 5,  
              'isDirectHadronDecayProduct': 6,  
              'isHardProcess': 7,
              'fromHardProcess': 8,  
              'isHardProcessTauDecayProduct': 9,
              'isDirectHardProcessTauDecayProduct': 10, 
              'fromHardProcessBeforeFSR': 11, 
              'isFirstCopy': 12, 
              'isLastCopy': 13, 
              'isLastCopyBeforeFSR': 14, 
        })

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        for variable in self.variables:
            btype = "F"
            if variable=='isPrompt' or variable=='isChargeFlip': btype = "O"
            if variable=='matchPdgId': btype = "I"
            self.out.branch('Electron_{}'.format(variable), btype, lenVar='nElectron')
            self.out.branch('Muon_{}'.format(variable), btype, lenVar='nMuon')

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        ### process a single event
        # (always return True as this module performs no selection)

        # get collections of particles for this event
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        genparticles = Collection(event, "GenPart")

        # do custom matching
        electron_matches = [self.findmatch(e, 11, genparticles) for e in electrons]
        muon_matches = [self.findmatch(m, 13, genparticles) for m in muons]

        # isPrompt
        if 'isPrompt' in self.variables:
            electron_isprompt = [self.genpart_is_prompt(g) for g in electron_matches]
            muon_isprompt = [self.genpart_is_prompt(g) for g in muon_matches]
            self.out.fillBranch('Electron_isPrompt', electron_isprompt)
            self.out.fillBranch('Muon_isPrompt', muon_isprompt)

        # matchPdgId
        if 'matchPdgId' in self.variables:
            electron_matchpdgid = [(g.pdgId if g is not None else 0) for g in electron_matches]
            muon_matchpdgid = [(g.pdgId if g is not None else 0) for g in muon_matches]
            self.out.fillBranch('Electron_matchPdgId', electron_matchpdgid)
            self.out.fillBranch('Muon_matchPdgId', muon_matchpdgid)

        if 'provenanceConversion' in self.variables:
            electron_provenance = [self.provenanceconversion(g, genparticles) for g in electron_matches]
            muon_provenance = [self.provenanceconversion(g, genparticles) for g in muon_matches]
            self.out.fillBranch('Electron_provenanceConversion', electron_provenance)
            self.out.fillBranch('Muon_provenanceConversion', muon_provenance)

        # motherPdgId
        if 'motherPdgId' in self.variables:
            electron_motherpdgid = [self.motherpdgid(g, genparticles) for g in electron_matches]
            muon_motherpdgid = [self.motherpdgid(g, genparticles) for g in muon_matches]
            self.out.fillBranch('Electron_motherPdgId', electron_motherpdgid)
            self.out.fillBranch('Muon_motherPdgId', muon_motherpdgid)

        # isChargeFlip
        if 'isChargeFlip' in self.variables:
            electron_ischargeflip = [False]*len(electrons)
            for i,(e,g) in enumerate(zip(electrons, electron_matches)):
                if g is None: continue
                if g.pdgId==-e.pdgId: electron_ischargeflip[i] = True
            muon_ischargeflip = [False]*len(muons)
            for i,(m,g) in enumerate(zip(muons, muon_matches)):
                if g is None: continue
                if g.pdgId==-m.pdgId: muon_ischargeflip[i] = True
            self.out.fillBranch('Electron_isChargeFlip', electron_ischargeflip)
            self.out.fillBranch('Muon_isChargeFlip', muon_ischargeflip)

        return True

    def genpart_has_status(self, genpart, status):
        ### internal helper function to determine if a gen particle has a given status
        # based on:
        # https://github.com/HEP-KBFI/tth-nanoAOD-tools/blob/
        # master/python/postprocessing/modules/genParticleProducer.py
        if genpart is None: return False
        if not status in self.statusmap:
            raise Exception('ERROR: status {} not recognized.'.format(status))
        return (genpart.statusFlags & (1 << self.statusmap[status]) != 0)

    def genpart_is_prompt(self, genpart):
        ### internal helper function to determine if a gen particle is prompt
        if genpart is None: return False
        isprompt = (
          self.genpart_has_status(genpart, 'isPrompt')
          or self.genpart_has_status(genpart, 'isDirectPromptTauDecayProduct')
          or self.genpart_has_status(genpart, 'isHardProcess')
          or self.genpart_has_status(genpart, 'fromHardProcess')
          or self.genpart_has_status(genpart, 'fromHardProcessBeforeFSR')
        )
        return isprompt

    def geometricmatch(self, recopart, recopartpdgid, genparts, allowphoton=False):
        ### internal helper function to determine geometric gen match,
        # in case the builtin gen matching is not valid.
        # based on:
        # https://github.com/LukaLambrecht/ewkino/blob/nanoaod/objects/src/LeptonGeneratorInfo.cc
        # which was in turn based on:
        # https://github.com/GhentAnalysis/heavyNeutrino/blob/UL_master/multilep/src/GenTools.cc

        # initialize
        match = None
        mindr = 99.

        # loop over gen particles
        for genpart in genparts:
            # decide whether gen particle has correct pdgid
            pdgidmask = abs(genpart.pdgId)==abs(recopartpdgid)
            if allowphoton: pdgidmask = (pdgidmask or abs(genpart.pdgId)==22)
            if not pdgidmask: continue
            # decide whether gen particle has correct status
            statusmask = (genpart.status==1)
            if abs(recopartpdgid)==15:
                statusmask = (genpart.status==2 and self.genpart_has_status('isLastCopy'))
                # (special case for taus)
            if not statusmask: continue

            # calculate delta R
            dr = recopart.DeltaR(genpart)
            if dr<mindr:
                match = genpart
                mindr = dr

        # repeat the procedure with allowing photons for cases without valid match so far
        if( mindr>0.2 ):
            if not allowphoton:
                match = self.geometricmatch(recopart, recopartpdgid, genparts, allowphoton=True)
            else: return None

        # return the result
        return match

    def findmatch(self, recopart, recopartpdgid, genparts):
        ### internal helper function to determine gen match.
        # priority is given on builtin matching, with fallback to geometric matching.
        validmatch = False
        if recopart.genPartIdx >= 0:
            genmatch = genparts[recopart.genPartIdx]
            validmatch = (genmatch.pdgId==recopart.pdgId)
        if not validmatch:
            genmatch = self.geometricmatch(recopart, recopartpdgid, genparts)
        return genmatch

    def provenanceconversion(self, photon, genparticles):
        # see https://github.com/GhentAnalysis/heavyNeutrino/blob/
        # cd101501001e9776b324002da585e38fe0a378d4/multilep/src/GenTools.cc#L191
        if photon is None: return 99
        if photon.pdgId != 22: return 99
        if not (self.genpart_has_status(photon, 'isPrompt') and photon.status == 1): return 2
        if photon.pt < 10: return 1
        for genpart in genparticles:
            if genpart.status != 23: continue
            partonId = abs(genpart.pdgId)
            if not ( (partonId == 21) or (partonId > 0 and partonId < 7) ): continue
            if photon.DeltaR(genpart) < 0.05: return 1
        return 0

    def motherpdgid(self, genpart, genparticles):
        """
        Returns the pdgId of the mother of a gen particle.
        GenPart is the generator particle matched to the reco particle. Can be None.
        """
        if genpart is None: return 0
        mother = self.getMother(genpart, genparticles)
        if mother:
            return mother.pdgId
        else:
            return 0

    def getMother(self, genpart, genparticles):
        """
        Returns the first mother of a gen particle.
        """
        if genpart.genPartIdxMother < 0: return None
        firstmother = genparticles[genpart.genPartIdxMother]
        if (firstmother.pdgId == genpart.pdgId): return self.getMother(firstmother, genparticles)
        return firstmother
