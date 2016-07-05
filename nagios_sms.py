#!/usr/bin/python
# -*- coding: utf-8 -*-

# Load Modules
import json, subprocess, requests
#########################
#                       #
#  Nagios status Check  #
#                       #
#########################
#
# 1. status.dat  to  json files
#    prompt>> npm install -g nagios-status-parser
#    prompt>> nagios-status-parser /usr/local/nagios/var/status.dat > A.txt
#
# 2. A.txt  python parsing
#
#

# Parsing JSON from status.dat
nagiStat = subprocess.check_output(['nagios-status-parser /usr/local/nagios/var/status.dat'], shell=True)
nagiPar = json.loads(nagiStat)

class nagiosStatParsing:

    def WAR(self):
        global nagiStat
        global nagiPar
        w_list = {}                                                             # Empty DIC

        for item in nagiPar["servicestatus"]:
            if 1 == item["current_state"]:                                      # current_state : 1 = WARNING
                w_list[item["host_name"]] = item["service_description"]         # Make Waring Dictionary

        print(w_list)

    def CRI(self):
        global nagiStat
        global nagiPar
        c_list = []                                                             # Empty list

        for item in nagiPar["servicestatus"]:
            if 2 == item["current_state"]:                                      # current_state : 2 = CRITICAL
                c_list.append(item["host_name"])
                #c_list[item["host_name"]] = item["service_description"]         # Make Critical list

        print(c_list)


## Checking LIST
e = nagiosStatParsing()
e.WAR()
e.CRI()

##############
#            #
#  Send SMS  #
#            #
##############

# GET 요청시
# http://sms.cyebiz.com/sms_send.php?type=sms&name=%EC%A1%B0%EC%97%B0%ED%98%B8&phone=01028241085&msg=TEST%20MESSAGE&callback=0263423352&apiKey=8a1b076d4da59d51eac3d59a2903c744

phone_number = '01028241085'
NagiosMSG = e.CRI()

def SendSMS(phone, nagiosMessage):
    url = 'http://sms.cyebiz.com/sms_send.php'

    payload = {
        'type':'sms',
        'returnurl':'',
        'reserve':'0',
        'name':'Nagios',
        'phone': phone,
        'msg': nagiosMessage,
        'callback':'0263423352',
        'apikey':'8a1b076d4da59d51eac3d59a2903c744',
        'etc1':'',
        'etc2':'',
        'timeout':'3'
    }
    r = requests.post(url, data=payload)

#SendSMS(phone_number, NagiosMSG)

