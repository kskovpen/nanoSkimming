#################################
# Definition of muon selections #
#################################

def muonselection(muon, selectionid=None):
    ### perform muon selection
    # input arguments:
    # - muon: nanoAODTools muon object
    # - selectionid: selection identifier
    # returns:
    # a boolean mask
    
    # switch between selections
    if( selectionid is None ): return (muon.pt > 0.)
    elif( selectionid=='run2ul_loose' ): return muonid_run2ul_loose(muon)

    # raise error if selection parameters are invalid
    msg = 'ERROR in muonelection:'
    msg += ' selection {} not recognized.'.format(selectionid)
    raise Exception(msg)


### loose selection for Run2 UL TOP lepton MVA based IDs
# references:
# - https://github.com/LukaLambrecht/ewkino/blob/
#   4f5a9908fe4a4b5899671738b1d73193e6a6a16c/objectSelection/MuonSelector.cc#L16
# - Kirill's AN on the TOP lepton MVA (AN-2022-016)

def muonid_run2ul_loose(muon):
    return (
        muon.isPFcand
        and (muon.isTracker or muon.isGlobal)
        and muon.pt > 7.
        and abs(muon.eta) < 2.4
        and abs(muon.dxy) < 0.05
        and abs(muon.dz) < 0.1
        and muon.sip3d < 8.
        and muon.miniPFRelIso_all < 0.4
        and muon.mediumId
    )
