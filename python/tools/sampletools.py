#############################
# Tools for sample handling #
#############################

def getsampleparams(sample):
    ### get year and data type for a given sample name
    # not guaranteed to be complete,
    # perhaps to extend when encountering more 'exotic' sample names...
    years = []
    dtypes = []
    if 'Run2016' in sample:
        years.append('2016')
        dtypes.append('data')
    if 'Run2017' in sample:
        years.append('2017')
        dtypes.append('data')
    if 'Run2018' in sample:
        years.append('2018')
        dtypes.append('data')
    if 'RunIISummer20UL16' in sample:
        years.append('2016')
        dtypes.append('sim')
    if 'RunIISummer20UL17' in sample:
        years.append('2017')
        dtypes.append('sim')
    if 'RunIISummer20UL18' in sample:
        years.append('2018')
        dtypes.append('sim')
    if len(set(years))!=1:
        msg = 'ERROR: could not determine year'
        msg += ' for sample {}, found candidates {}'.format(sample, years)
        raise Exception(msg)
    if len(set(dtypes))!=1:
        msg = 'ERROR: could not determine data type'
        msg += ' for sample {}, found candidates {}'.format(sample, dtypes)
        raise Exception(msg)
    
    ret = {'year': years[0], 'dtype': dtypes[0]}
    if ret['dtype'] == 'data':
        # split on "Run" and take last part
        runperiod = sample.split("Run")[-1][4]
        # assert runperiod is a capitalized letter:
        if not runperiod.isupper():
            msg = 'ERROR: could not determine run period'
            msg += ' for sample {}'.format(sample)
            msg += " Make sure sample name for data follows Run[YEAR][PERIOD] 
            msg += "format with period a single capital letter for the era.""
            raise Exception(msg)
        ret['runperiod'] = runperiod
    else:
        ret['runperiod'] = "B"

    return ret
