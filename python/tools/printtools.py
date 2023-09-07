######################################################
# Tools for easier printing of NanoAOD-Tools objects #
######################################################

def leptontostr(lepton):
    lstr = 'Lepton: '
    lstr += ', isPFCand={}'.format( lepton.isPFcand )
    lstr += ', pt={}'.format( lepton.pt )
    lstr += ', eta={}'.format( lepton.eta )
    lstr += ', dxy={}'.format( lepton.dxy )
    lstr += ', dz={}'.format( lepton.dz )
    lstr += ', sip3d={}'.format( lepton.sip3d )
    lstr += ', miniPFRelIso_all={}'.format( lepton.miniPFRelIso_all )
    return lstr

def muontostr(muon):
    mstr = leptontostr(muon)
    mstr = 'Muon: ' + mstr
    return mstr

def electrontostr(electron):
    estr = leptontostr(electron)
    estr = 'Electron: ' + estr
    return estr
