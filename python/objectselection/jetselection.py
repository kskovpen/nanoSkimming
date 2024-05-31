################################
# Definition of jet selections #
################################

def jetselection(jet, selectionid=None):
    ### perform jet selection
    # input arguments:
    # - jet: nanoAODTools jet object
    # - selectionid: selection identifier
    # returns:
    # a boolean
    
    # switch between selections
    if( selectionid is None ): return (jet.pt > 0.)
    elif( selectionid=='run2ul_default'): return jetid_run2ul_default(jet)
    
    # raise error if selection parameters are invalid
    msg = 'ERROR in jetelection:'
    msg += ' selection {} not recognized.'.format(selectionid)
    raise Exception(msg)


### default jet ID for Run 2 UL analyses ###

def jetid_run2ul_default(jet):
    return (
        jet.pt > 25.
        and abs(jet.eta) < 2.4
        and jet.isTight
    )
