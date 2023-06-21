import os
import sys


def getlumijson(year):
    json = None
    jsonbase = 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/'
    if year=='2016':
        json = (jsonbase 
                + 'Collisions16/13TeV/Legacy_2016/'
                + 'Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt')
    if year=='2017':
        json = (jsonbase
                + 'Collisions17/13TeV/Legacy_2017/'
                + 'Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt')
    if year=='2018':
        json = (jsonbase
                + 'Collisions18/13TeV/Legacy_2018/'
                + 'Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt')
    if json is None:
        msg = 'ERROR in getlumijson: year {} not recognized.'.format(year)
        raise Exception(msg)
    return json


if __name__=='__main__':

    for year in ['2016','2017','2018']:
        url = getlumijson(year)
        filename = 'lumijson_{}.json'.format(year)
        cmd = 'curl -o {} {}'.format(filename, url)
        os.system(cmd)
