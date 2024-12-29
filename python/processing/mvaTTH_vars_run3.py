"""
Define dictionaries for muon evaluators
"""
import array as ar
import numpy as np

class MVAvar:
    def __init__(self, name):
        self.name = name
        self.var = ar.array('f', [0.])
    
    def set(self, val):
        self.var[0] = val

def muon_df(year):
    vars_muons_jetdf  = {
        "Muon_pt" : 
            [MVAvar("Muon_pt"), lambda lep, jets: lep.pt],
        "Muon_eta" : 
            [MVAvar("Muon_eta"), lambda lep, jets: lep.eta],
        "Muon_pfRelIso03_all" : 
            [MVAvar("Muon_pfRelIso03_all"), lambda lep, jets: lep.pfRelIso03_all],
        "Muon_miniPFRelIso_chg" : 
            [MVAvar("Muon_miniPFRelIso_chg"), lambda lep, jets: lep.miniPFRelIso_chg ],
        "Muon_miniRelIsoNeutral := Muon_miniPFRelIso_all - Muon_miniPFRelIso_chg" :
            [MVAvar("Muon_miniRelIsoNeutral := Muon_miniPFRelIso_all - Muon_miniPFRelIso_chg"), lambda lep, jets: lep.miniPFRelIso_all - lep.miniPFRelIso_chg],
        "Muon_jetNDauCharged" :
            [MVAvar("Muon_jetNDauCharged"), lambda lep, jets: lep.jetNDauCharged],
        "Muon_jetPtRelv2" :
            [MVAvar("Muon_jetPtRelv2"), lambda lep, jets: lep.jetPtRelv2],
        "Muon_jetBTagDeepFlavB := Muon_jetIdx > -1 ? Jet_btagDeepFlavB[Muon_jetIdx] : 0" : 
            [MVAvar("Muon_jetBTagDeepFlavB := Muon_jetIdx > -1 ? Jet_btagDeepFlavB[Muon_jetIdx] : 0"), lambda lep, jets: jets[lep.jetIdx].btagDeepFlavB if lep.jetIdx > -1 else 0],
        "Muon_jetPtRatio := min(1 / (1 + Muon_jetRelIso), 1.5)" : 
            [MVAvar("Muon_jetPtRatio := min(1 / (1 + Muon_jetRelIso), 1.5)"), lambda lep, jets: min(1. / (1. + lep.jetRelIso), 1.5) ],
        "Muon_sip3d" : 
            [MVAvar("Muon_sip3d"), lambda lep, jets: lep.sip3d],
        "Muon_log_dxy := log(abs(Muon_dxy))" :
            [MVAvar("Muon_log_dxy := log(abs(Muon_dxy))"), lambda lep, jets: np.log(abs(lep.dxy))],
        "Muon_log_dz  := log(abs(Muon_dz))" : 
            [MVAvar("Muon_log_dz  := log(abs(Muon_dz))"), lambda lep, jets: np.log(abs(lep.dz))],
        "Muon_segmentComp" : 
            [MVAvar("Muon_segmentComp"),lambda lep, jets: lep.segmentComp],
    }

    return vars_muons_jetdf

def muon_pnet(year):
    vars_muons_jetpnet  = {
        "Muon_pt" : 
            [MVAvar("Muon_pt"), lambda lep, jets: lep.pt],
        "Muon_eta" : 
            [MVAvar("Muon_eta"), lambda lep, jets: lep.eta],
        "Muon_pfRelIso03_all" : 
            [MVAvar("Muon_pfRelIso03_all"), lambda lep, jets: lep.pfRelIso03_all],
        "Muon_miniPFRelIso_chg" : 
            [MVAvar("Muon_miniPFRelIso_chg"), lambda lep, jets: lep.miniPFRelIso_chg ],
        "Muon_miniRelIsoNeutral := Muon_miniPFRelIso_all - Muon_miniPFRelIso_chg" :
            [MVAvar("Muon_miniRelIsoNeutral := Muon_miniPFRelIso_all - Muon_miniPFRelIso_chg"), lambda lep, jets: lep.miniPFRelIso_all - lep.miniPFRelIso_chg],
        "Muon_jetNDauCharged" :
            [MVAvar("Muon_jetNDauCharged"), lambda lep, jets: lep.jetNDauCharged],
        "Muon_jetPtRelv2" :
            [MVAvar("Muon_jetPtRelv2"), lambda lep, jets: lep.jetPtRelv2],
        "Muon_jetBTagPNET := Muon_jetIdx > -1 ? Jet_btagPNetB[Muon_jetIdx] : 0" : 
            [MVAvar("Muon_jetBTagPNET := Muon_jetIdx > -1 ? Jet_btagPNetB[Muon_jetIdx] : 0"), lambda lep, jets: jets[lep.jetIdx].btagPNetB if lep.jetIdx > -1 else 0],
        "Muon_jetPtRatio := min(1 / (1 + Muon_jetRelIso), 1.5)" : 
            [MVAvar("Muon_jetPtRatio := min(1 / (1 + Muon_jetRelIso), 1.5)"), lambda lep, jets: min(1. / (1. + lep.jetRelIso), 1.5) ],
        "Muon_sip3d" : 
            [MVAvar("Muon_sip3d"), lambda lep, jets: lep.sip3d],
        "Muon_log_dxy := log(abs(Muon_dxy))" :
            [MVAvar("Muon_log_dxy := log(abs(Muon_dxy))"), lambda lep, jets: np.log(abs(lep.dxy))],
        "Muon_log_dz  := log(abs(Muon_dz))" : 
            [MVAvar("Muon_log_dz  := log(abs(Muon_dz))"), lambda lep, jets: np.log(abs(lep.dz))],
        "Muon_segmentComp" : 
            [MVAvar("Muon_segmentComp"),lambda lep, jets: lep.segmentComp],
    }


    return vars_muons_jetpnet

def electron_pnet_wNoIso(year):
    vars_electron_pnet_wNoIso  = {
        "Electron_pt" : 
            [MVAvar("Electron_pt"), lambda lep, jets: lep.pt],
        "Electron_eta" : 
            [MVAvar("Electron_eta"), lambda lep, jets: lep.eta],
        "Electron_pfRelIso03_all" : 
            [MVAvar("Electron_pfRelIso03_all"), lambda lep, jets: lep.pfRelIso03_all],
        "Electron_miniPFRelIso_chg" : 
            [MVAvar("Electron_miniPFRelIso_chg"), lambda lep, jets: lep.miniPFRelIso_chg ],
        "Electron_miniRelIsoNeutral := Electron_miniPFRelIso_all - Electron_miniPFRelIso_chg" :
            [MVAvar("Electron_miniRelIsoNeutral := Electron_miniPFRelIso_all - Electron_miniPFRelIso_chg"), lambda lep, jets: lep.miniPFRelIso_all - lep.miniPFRelIso_chg],
        "Electron_jetNDauCharged" :
            [MVAvar("Electron_jetNDauCharged"), lambda lep, jets: lep.jetNDauCharged],
        "Electron_jetPtRelv2" :
            [MVAvar("Electron_jetPtRelv2"), lambda lep, jets: lep.jetPtRelv2],
        "Electron_jetBTagPNET := Electron_jetIdx > -1 ? Jet_btagPNetB[Electron_jetIdx] : 0" : 
            [MVAvar("Electron_jetBTagPNET := Electron_jetIdx > -1 ? Jet_btagPNetB[Electron_jetIdx] : 0"), lambda lep, jets: jets[lep.jetIdx].btagPNetB if lep.jetIdx > -1 else 0],
        "Electron_jetPtRatio := min(1 / (1 + Electron_jetRelIso), 1.5)" : 
            [MVAvar("Electron_jetPtRatio := min(1 / (1 + Electron_jetRelIso), 1.5)"), lambda lep, jets: min(1. / (1. + lep.jetRelIso), 1.5) ],
        "Electron_sip3d" : 
            [MVAvar("Electron_sip3d"), lambda lep, jets: lep.sip3d],
        "Electron_log_dxy := log(abs(Electron_dxy))" :
            [MVAvar("Electron_log_dxy := log(abs(Electron_dxy))"), lambda lep, jets: np.log(abs(lep.dxy))],
        "Electron_log_dz  := log(abs(Electron_dz))" : 
            [MVAvar("Electron_log_dz  := log(abs(Electron_dz))"), lambda lep, jets: np.log(abs(lep.dz))],
        "Electron_mvaNoIso" : 
            [MVAvar("Electron_mvaNoIso"),lambda lep, jets: lep.mvaNoIso],
    }


    return vars_electron_pnet_wNoIso

def electron_pnet_wIso(year):
    vars_electron_pnet_wIso  = {
        "Electron_pt" : 
            [MVAvar("Electron_pt"), lambda lep, jets: lep.pt],
        "Electron_eta" : 
            [MVAvar("Electron_eta"), lambda lep, jets: lep.eta],
        "Electron_pfRelIso03_all" : 
            [MVAvar("Electron_pfRelIso03_all"), lambda lep, jets: lep.pfRelIso03_all],
        "Electron_miniPFRelIso_chg" : 
            [MVAvar("Electron_miniPFRelIso_chg"), lambda lep, jets: lep.miniPFRelIso_chg ],
        "Electron_miniRelIsoNeutral := Electron_miniPFRelIso_all - Electron_miniPFRelIso_chg" :
            [MVAvar("Electron_miniRelIsoNeutral := Electron_miniPFRelIso_all - Electron_miniPFRelIso_chg"), lambda lep, jets: lep.miniPFRelIso_all - lep.miniPFRelIso_chg],
        "Electron_jetNDauCharged" :
            [MVAvar("Electron_jetNDauCharged"), lambda lep, jets: lep.jetNDauCharged],
        "Electron_jetPtRelv2" :
            [MVAvar("Electron_jetPtRelv2"), lambda lep, jets: lep.jetPtRelv2],
        "Electron_jetBTagPNET := Electron_jetIdx > -1 ? Jet_btagPNetB[Electron_jetIdx] : 0" : 
            [MVAvar("Electron_jetBTagPNET := Electron_jetIdx > -1 ? Jet_btagPNetB[Electron_jetIdx] : 0"), lambda lep, jets: jets[lep.jetIdx].btagPNetB if lep.jetIdx > -1 else 0],
        "Electron_jetPtRatio := min(1 / (1 + Electron_jetRelIso), 1.5)" : 
            [MVAvar("Electron_jetPtRatio := min(1 / (1 + Electron_jetRelIso), 1.5)"), lambda lep, jets: min(1. / (1. + lep.jetRelIso), 1.5) ],
        "Electron_sip3d" : 
            [MVAvar("Electron_sip3d"), lambda lep, jets: lep.sip3d],
        "Electron_log_dxy := log(abs(Electron_dxy))" :
            [MVAvar("Electron_log_dxy := log(abs(Electron_dxy))"), lambda lep, jets: np.log(abs(lep.dxy))],
        "Electron_log_dz  := log(abs(Electron_dz))" : 
            [MVAvar("Electron_log_dz  := log(abs(Electron_dz))"), lambda lep, jets: np.log(abs(lep.dz))],
        "Electron_mvaNoIso" : 
            [MVAvar("Electron_mvaIso"),lambda lep, jets: lep.mvaIso],
    }

    return vars_electron_pnet_wIso


def electron_df_wNoIso(year):
    vars_electron_df_wNoIso  = {
        "Electron_pt" : 
            [MVAvar("Electron_pt"), lambda lep, jets: lep.pt],
        "Electron_eta" : 
            [MVAvar("Electron_eta"), lambda lep, jets: lep.eta],
        "Electron_pfRelIso03_all" : 
            [MVAvar("Electron_pfRelIso03_all"), lambda lep, jets: lep.pfRelIso03_all],
        "Electron_miniPFRelIso_chg" : 
            [MVAvar("Electron_miniPFRelIso_chg"), lambda lep, jets: lep.miniPFRelIso_chg ],
        "Electron_miniRelIsoNeutral := Electron_miniPFRelIso_all - Electron_miniPFRelIso_chg" :
            [MVAvar("Electron_miniRelIsoNeutral := Electron_miniPFRelIso_all - Electron_miniPFRelIso_chg"), lambda lep, jets: lep.miniPFRelIso_all - lep.miniPFRelIso_chg],
        "Electron_jetNDauCharged" :
            [MVAvar("Electron_jetNDauCharged"), lambda lep, jets: lep.jetNDauCharged],
        "Electron_jetPtRelv2" :
            [MVAvar("Electron_jetPtRelv2"), lambda lep, jets: lep.jetPtRelv2],
        "Electron_jetBTagDeepFlavB := Electron_jetIdx > -1 ? Jet_btagDeepFlavB[Electron_jetIdx] : 0" : 
            [MVAvar("Electron_jetBTagDeepFlavB := Electron_jetIdx > -1 ? Jet_btagDeepFlavB[Electron_jetIdx] : 0"), lambda lep, jets: jets[lep.jetIdx].btagDeepFlavB if lep.jetIdx > -1 else 0],
        "Electron_jetPtRatio := min(1 / (1 + Electron_jetRelIso), 1.5)" : 
            [MVAvar("Electron_jetPtRatio := min(1 / (1 + Electron_jetRelIso), 1.5)"), lambda lep, jets: min(1. / (1. + lep.jetRelIso), 1.5) ],
        "Electron_sip3d" : 
            [MVAvar("Electron_sip3d"), lambda lep, jets: lep.sip3d],
        "Electron_log_dxy := log(abs(Electron_dxy))" :
            [MVAvar("Electron_log_dxy := log(abs(Electron_dxy))"), lambda lep, jets: np.log(abs(lep.dxy))],
        "Electron_log_dz  := log(abs(Electron_dz))" : 
            [MVAvar("Electron_log_dz  := log(abs(Electron_dz))"), lambda lep, jets: np.log(abs(lep.dz))],
        "Electron_mvaNoIso" : 
            [MVAvar("Electron_mvaNoIso"),lambda lep, jets: lep.mvaNoIso],
    }


    return vars_electron_df_wNoIso

def electron_df_wIso(year):
    vars_electron_df_wIso  = {
        "Electron_pt" : 
            [MVAvar("Electron_pt"), lambda lep, jets: lep.pt],
        "Electron_eta" : 
            [MVAvar("Electron_eta"), lambda lep, jets: lep.eta],
        "Electron_pfRelIso03_all" : 
            [MVAvar("Electron_pfRelIso03_all"), lambda lep, jets: lep.pfRelIso03_all],
        "Electron_miniPFRelIso_chg" : 
            [MVAvar("Electron_miniPFRelIso_chg"), lambda lep, jets: lep.miniPFRelIso_chg ],
        "Electron_miniRelIsoNeutral := Electron_miniPFRelIso_all - Electron_miniPFRelIso_chg" :
            [MVAvar("Electron_miniRelIsoNeutral := Electron_miniPFRelIso_all - Electron_miniPFRelIso_chg"), lambda lep, jets: lep.miniPFRelIso_all - lep.miniPFRelIso_chg],
        "Electron_jetNDauCharged" :
            [MVAvar("Electron_jetNDauCharged"), lambda lep, jets: lep.jetNDauCharged],
        "Electron_jetPtRelv2" :
            [MVAvar("Electron_jetPtRelv2"), lambda lep, jets: lep.jetPtRelv2],
        "Electron_jetBTagDeepFlavB := Electron_jetIdx > -1 ? Jet_btagDeepFlavB[Electron_jetIdx] : 0" : 
            [MVAvar("Electron_jetBTagDeepFlavB := Electron_jetIdx > -1 ? Jet_btagDeepFlavB[Electron_jetIdx] : 0"), lambda lep, jets: jets[lep.jetIdx].btagDeepFlavB if lep.jetIdx > -1 else 0],
        "Electron_jetPtRatio := min(1 / (1 + Electron_jetRelIso), 1.5)" : 
            [MVAvar("Electron_jetPtRatio := min(1 / (1 + Electron_jetRelIso), 1.5)"), lambda lep, jets: min(1. / (1. + lep.jetRelIso), 1.5) ],
        "Electron_sip3d" : 
            [MVAvar("Electron_sip3d"), lambda lep, jets: lep.sip3d],
        "Electron_log_dxy := log(abs(Electron_dxy))" :
            [MVAvar("Electron_log_dxy := log(abs(Electron_dxy))"), lambda lep, jets: np.log(abs(lep.dxy))],
        "Electron_log_dz  := log(abs(Electron_dz))" : 
            [MVAvar("Electron_log_dz  := log(abs(Electron_dz))"), lambda lep, jets: np.log(abs(lep.dz))],
        "Electron_mvaNoIso" : 
            [MVAvar("Electron_mvaIso"),lambda lep, jets: lep.mvaIso],
    }


    return vars_electron_df_wIso


def electron_pnet(year):
    vars_electron_pnet  = {
        "Electron_pt" : 
            [MVAvar("Electron_pt"), lambda lep, jets: lep.pt],
        "Electron_eta" : 
            [MVAvar("Electron_eta"), lambda lep, jets: lep.eta],
        "Electron_pfRelIso03_all" : 
            [MVAvar("Electron_pfRelIso03_all"), lambda lep, jets: lep.pfRelIso03_all],
        "Electron_miniPFRelIso_chg" : 
            [MVAvar("Electron_miniPFRelIso_chg"), lambda lep, jets: lep.miniPFRelIso_chg ],
        "Electron_miniRelIsoNeutral := Electron_miniPFRelIso_all - Electron_miniPFRelIso_chg" :
            [MVAvar("Electron_miniRelIsoNeutral := Electron_miniPFRelIso_all - Electron_miniPFRelIso_chg"), lambda lep, jets: lep.miniPFRelIso_all - lep.miniPFRelIso_chg],
        "Electron_jetNDauCharged" :
            [MVAvar("Electron_jetNDauCharged"), lambda lep, jets: lep.jetNDauCharged],
        "Electron_jetPtRelv2" :
            [MVAvar("Electron_jetPtRelv2"), lambda lep, jets: lep.jetPtRelv2],
        "Electron_jetBTagPNET := Electron_jetIdx > -1 ? Jet_btagPNetB[Electron_jetIdx] : 0" : 
            [MVAvar("Electron_jetBTagPNET := Electron_jetIdx > -1 ? Jet_btagPNetB[Electron_jetIdx] : 0"), lambda lep, jets: jets[lep.jetIdx].btagPNetB if lep.jetIdx > -1 else 0],
        "Electron_jetPtRatio := min(1 / (1 + Electron_jetRelIso), 1.5)" : 
            [MVAvar("Electron_jetPtRatio := min(1 / (1 + Electron_jetRelIso), 1.5)"), lambda lep, jets: min(1. / (1. + lep.jetRelIso), 1.5) ],
        "Electron_sip3d" : 
            [MVAvar("Electron_sip3d"), lambda lep, jets: lep.sip3d],
        "Electron_log_dxy := log(abs(Electron_dxy))" :
            [MVAvar("Electron_log_dxy := log(abs(Electron_dxy))"), lambda lep, jets: np.log(abs(lep.dxy))],
        "Electron_log_dz  := log(abs(Electron_dz))" : 
            [MVAvar("Electron_log_dz  := log(abs(Electron_dz))"), lambda lep, jets: np.log(abs(lep.dz))],
    }


    return vars_electron_pnet

def electron_df(year):
    vars_electron_df  = {
        "Electron_pt" : 
            [MVAvar("Electron_pt"), lambda lep, jets: lep.pt],
        "Electron_eta" : 
            [MVAvar("Electron_eta"), lambda lep, jets: lep.eta],
        "Electron_pfRelIso03_all" : 
            [MVAvar("Electron_pfRelIso03_all"), lambda lep, jets: lep.pfRelIso03_all],
        "Electron_miniPFRelIso_chg" : 
            [MVAvar("Electron_miniPFRelIso_chg"), lambda lep, jets: lep.miniPFRelIso_chg ],
        "Electron_miniRelIsoNeutral := Electron_miniPFRelIso_all - Electron_miniPFRelIso_chg" :
            [MVAvar("Electron_miniRelIsoNeutral := Electron_miniPFRelIso_all - Electron_miniPFRelIso_chg"), lambda lep, jets: lep.miniPFRelIso_all - lep.miniPFRelIso_chg],
        "Electron_jetNDauCharged" :
            [MVAvar("Electron_jetNDauCharged"), lambda lep, jets: lep.jetNDauCharged],
        "Electron_jetPtRelv2" :
            [MVAvar("Electron_jetPtRelv2"), lambda lep, jets: lep.jetPtRelv2],
        "Electron_jetBTagDeepFlavB := Electron_jetIdx > -1 ? Jet_btagDeepFlavB[Electron_jetIdx] : 0" : 
            [MVAvar("Electron_jetBTagDeepFlavB := Electron_jetIdx > -1 ? Jet_btagDeepFlavB[Electron_jetIdx] : 0"), lambda lep, jets: jets[lep.jetIdx].btagDeepFlavB if lep.jetIdx > -1 else 0],
        "Electron_jetPtRatio := min(1 / (1 + Electron_jetRelIso), 1.5)" : 
            [MVAvar("Electron_jetPtRatio := min(1 / (1 + Electron_jetRelIso), 1.5)"), lambda lep, jets: min(1. / (1. + lep.jetRelIso), 1.5) ],
        "Electron_sip3d" : 
            [MVAvar("Electron_sip3d"), lambda lep, jets: lep.sip3d],
        "Electron_log_dxy := log(abs(Electron_dxy))" :
            [MVAvar("Electron_log_dxy := log(abs(Electron_dxy))"), lambda lep, jets: np.log(abs(lep.dxy))],
        "Electron_log_dz  := log(abs(Electron_dz))" : 
            [MVAvar("Electron_log_dz  := log(abs(Electron_dz))"), lambda lep, jets: np.log(abs(lep.dz))],
    }

    return vars_electron_df
