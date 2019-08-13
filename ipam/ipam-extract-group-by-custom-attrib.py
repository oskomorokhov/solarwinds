"""
query solarwinds IPAM based on custom-attribute name/value, extract required data
"""

import orionsdk
import configparser

config = configparser.ConfigParser()
config.read('.credentials/work.ini') 

swis = orionsdk.SwisClient(config['orion']['host'],config['orion']['user'],config['orion']['pass'])
data=swis.query("Select Address,CIDR,Location from IPAM.GroupNode gn INNER JOIN IPAM.GroupNodeAttr gna on gn.GroupID=gna.GroupID where gna.IsPublicIPAddress='yes'" )
data = [x for x in data if x['Address'] is not None]

result = {}

for entry in data:
    if entry['Location'] in result.keys():
        result[entry['Location']].add(entry['Address']+'/'+str(entry['CIDR']))
    else:
        result[entry['Location']] = set()
        result[entry['Location']].add(entry['Address']+'/'+str(entry['CIDR']))

txt = set([entry['Address']+'/'+str(entry['CIDR'])+' #'+str(entry['Location']) for entry in data])