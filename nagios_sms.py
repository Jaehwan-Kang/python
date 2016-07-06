#!/usr/bin/python
# -*- coding: utf-8 -*-
#
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
#    prompt>> nagios-status-parser /usr/local/nagios/var/status.dat
#
# 2.
#
#

# Nagios Status Class
class nagiosStatParsing:
    def WAR(self):
        global nagiPar
        w_list = []                                                             # Empty list
        for item in nagiPar["servicestatus"]:
            if 1 == item["current_state"]:                                      # current_state : 1 = WARNING
                w_list.append(item["host_name"])                                # Make Waring List
        return w_list

    def CRI(self):
        global nagiPar
        c_list = []                                                             # Empty list
        for item in nagiPar["servicestatus"]:
            if 2 == item["current_state"]:                                      # current_state : 2 = CRITICAL
                c_list.append(item["host_name"])                                # Make Critical List
        return c_list

# Check && DATA Insert
def status(chk):
    if 0 < len(chk):
        print(chk)
    else:
        print(" 0 ")

# Parsing JSON from status.dat
nagiStat = subprocess.check_output(['nagios-status-parser /usr/local/nagios/var/status.dat'], shell=True)
nagiPar = json.loads(nagiStat)

# Export list
e = nagiosStatParsing()
W = e.WAR()
C = e.CRI()

# Check status
status(W)
status(C)


##############
#            #
#  Send SMS  #
#            #
##############

# GET 요청시
# http://sms.cyebiz.com/sms_send.php?type=sms&name=%EC%A1%B0%EC%97%B0%ED%98%B8&phone=01028241085&msg=TEST%20MESSAGE&callback=0263423352&apiKey=8a1b076d4da59d51eac3d59a2903c744

phone_number = '01028241085'
#NagiosMSG = e.CRI()
NagiosMSG = 'Wow Sssssss'

def SendSMS(phone, nagiosMessage):
    url = 'http://sms.cyebiz.com/sms_send.php'

    postdata = {
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
    r = requests.post(url, data=postdata)

#SendSMS(phone_number, NagiosMSG)

