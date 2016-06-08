#! /usr/bin/python
# -*- coding: utf-8 -*-
#
# Usage
# #python check_haproxy_stat.py [URL] [USER] [PASSWORD] [LISTENER]
#
import sys
from haproxystats import HAProxyServer

haproxy = HAProxyServer(sys.argv[1], sys.argv[2], sys.argv[3], timeout=3)

listner = {}

for b in haproxy.listeners:
    listner[b.name] = b.status

try:
    if sys.argv[4] in listner:

        if listner[sys.argv[4]] == "UP":
            print("%s : %s" % (sys.argv[4], listner[sys.argv[4]]))
            sys.exit(0)  # OK exit code
        elif listner[sys.argv[4]] == "DOWN":
            print("%s : %s" % (sys.argv[4], listner[sys.argv[4]]))
            sys.exit(2)  # Critical exit code
        else:
            print("UNKNOWN %s : %s" % (sys.argv[4], listner[sys.argv[4]]))
            sys.exit(3)  # Unknown exit code

    else:
        print("Not Matched Listner : %s" % sys.argv[4])
        sys.exit(3) # Unknown exit code

except IndexError as e:
    print("Not Matched Arguments")
    sys.exit(3) # Unknown exit code
