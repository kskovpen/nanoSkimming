###############################
# Definition of b-tagged jet #
###############################

def inbtagacceptance(jet):
    ### internal helper function
    # todo: verify if these selections still correspond
    #       to the maximum acceptance of b-tagging algorithms.
    return ( jet.pt > 25. and abs(jet.eta)<2.4 )

def bjetelection(jet, year=None, algo=None, level=None):
    ### perform b-jet selection
    # input arguments:
    # - jet: nanoAODTools jet object
    # - year: year identifier for the provided jet
    # - algo: b-tagging algorithm (for now only 'deepflavor' is supported)
    # - level: choose from 'loose', 'medium' or 'tight'
    # returns:
    # a boolean

    # check arguments
    if( year is None or algo is None or level is None ):
        msg = 'ERROR in bjetelection:'
        msg += ' year, algo and level must all be provided.'
        raise Exception(msg)

    # switch between algorithms
    if( algo=='deepflavor' ): return deepflavorselection(jet, year, level)
    
    # raise error if b-tag algorithm is invalid
    msg = 'ERROR in bjetelection:'
    msg += ' algo {} not recognized.'.format(algo)
    raise Exception(msg)


### DeepJet/DeepFlavor b-tagging ###

def deepflavorselection(jet, year, level):
    ### perform b-jet selection using the DeepJet/DeepFlavor algorithm
    # note: the threshold values can be found here:
    #       https://btv-wiki.docs.cern.ch/ScaleFactors/UL2016preVFP/
    #       (and similar for other years)
    if not inbtagacceptance(jet): return False
    bscore = jet.btagDeepFlavB
    if year=='2016PreVFP':
        if level=='loose': return (bscore > 0.0508)
        if level=='medium': return (bscore > 0.2598)
        if level=='tight': return (bscore > 0.6502)
    if year=='2016PostVFP':
        if level=='loose': return (bscore > 0.0480)
        if level=='medium': return (bscore > 0.2489)
        if level=='tight': return (bscore > 0.6377)
    if year=='2017':
        if level=='loose': return (bscore > 0.0532)
        if level=='medium': return (bscore > 0.3040)
        if level=='tight': return (bscore > 0.7476)
    if year=='2018':
        if level=='loose': return (bscore > 0.0490)
        if level=='medium': return (bscore > 0.2783)
        if level=='tight': return (bscore > 0.7100)
    msg = 'ERROR in deepflavorselection:'
    msg += ' year {}, level {} not recognized.'.format(year, level)
    raise Exception(msg)
