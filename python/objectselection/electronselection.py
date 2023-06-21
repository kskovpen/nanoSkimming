#####################################
# Definition of electron selections #
#####################################

def electronselection(electron, selectionid=None):
    ### perform electron selection
    # input arguments:
    # - electron: nanoAODTools electron object
    # - selectionid: selection identifier
    # returns:
    # a boolean
    
    # switch between selections
    if( selectionid is None ): return (electron.pt > 0.)
    elif( selectionid=='run2ul_loose' ): return electronid_run2ul_loose(electron)
    
    # raise error if selection parameters are invalid
    msg = 'ERROR in electronelection:'
    msg += ' selection {} not recognized.'.format(selectionid)
    raise Exception(msg)


### loose selection for Run2 UL TOP lepton MVA based IDs
# references:
# - https://github.com/LukaLambrecht/ewkino/blob/
#   4f5a9908fe4a4b5899671738b1d73193e6a6a16c/objectSelection/ElectronSelector.cc#L20
# - Kirill's AN on the TOP lepton MVAand AN-2022-016)

def electronid_run2ul_loose(electron):
    return (electron.isPFcand
            and electron.pt > 10.
            and abs(electron.eta) < 2.5
            and abs(electron.dxy) < 0.05
            and abs(electron.dz) < 0.1
            and electron.sip3d < 8.
            and electron.lostHits < 2
            and electron.miniPFRelIso_all < 0.4
            and (abs(electron.eta + electron.deltaEtaSC) < 1.4442
                or abs(electron.eta + electron.deltaEtaSC) > 1.566) 
    )
