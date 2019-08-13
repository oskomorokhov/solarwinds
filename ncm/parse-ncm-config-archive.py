"""
Query solarwinds NCM based on device type or other criteria, parse config, extract required data
"""


import re
import ipaddress
import sys
from os import environ
import orionsdk
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

swis=orionsdk.SwisClient(environ['SW_SERVER'],environ['SW_USER'],environ['SW_PASS'])

device_types=['vg0','ir0','er0']

devices=[]

for device_type in device_types:
        result=swis.query(f"select SysName from NCM.Nodes where SysName like '%{device_type}%'")
        devices.extend([x['SysName'] for x in result['results']])

for device in devices:

    cfgs=swis.query(f"select A.NodeID,A.SysName,B.Config from NCM.Nodes A INNER JOIN Cirrus.ConfigArchive B on A.NodeID=B.NodeID where A.SysName='{device}' ORDER BY B.DownloadTime")

    cfgs=cfgs['results'][-1]['Config']

    cfg=re.findall(r'ipv4\s(\d.+)\r',cfgs)

    for ip in cfg:
        print(ipaddress.IPv4Network(ip.replace(' ','/')))