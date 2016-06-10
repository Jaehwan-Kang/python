#! /usr/bin/python
# -*- coding: utf-8 -*-
#
# Usage)python check_haproxy_stat.py [IP] [URL] [USER] [PASSWORD] [PXNAME]
#
# Nagios)check_haproxy_stat.py $HOSTADDRESS$ [URL] [USER] [PASSWORD] [PXNAME]

import sys
import json
from haproxystats import HAProxyServer

haproxy = HAProxyServer(sys.argv[2], sys.argv[3], sys.argv[4],timeout=3)

def CheckService(HaproxyIP,PXname):

    B = json.loads(haproxy.to_json())
    lists = {}
    for feed in B[HaproxyIP]["backends"]:
        if PXname == feed["pxname"]:
            for host in feed["listeners"]:
                lists[host["svname"]] = host["status"]

    if len(lists) == 0:
        print("Not Matched %s " % PXname)
        sys.exit(0)  # UNKNOWN exit code

    statlist = []
    for values in lists:
        if lists[values] == "DOWN":
            statlist.append(values)

    if len(statlist) != 0:
        print("PXname DOWN is %s" % statlist)
        sys.exit(2) # Critical exit code

    else:
        print("Service OK %s" % PXname)

CheckService(sys.argv[1], sys.argv[5])