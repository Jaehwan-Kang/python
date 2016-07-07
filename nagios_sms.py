#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Load Modules
import json, subprocess, requests, sqlite3
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

# Sqlite3 Query
real_query = "select count(*) from sqlite_master Where Name = '%s'"
create_query = "create table %s (No INTEGER PRIMARY KEY AUTOINCREMENT, State_code varchar (10), Date datetime default (datetime('now','localtime')))"
insert_w_query = "insert into %s (State_code) values ('w')"
insert_c_query = "insert into %s (State_code) values ('c')"
table_query = "SELECT name FROM sqlite_master WHERE type IN ('table', 'view') AND name NOT LIKE 'sqlite_%' UNION ALL SELECT name FROM sqlite_temp_master WHERE type IN ('table', 'view') ORDER BY 1"
null_query = "insert into %s (State_code) values('');"

class sqlitedb:
    def wUpdate(self, G):                               # Warning Update
        conn = sqlite3.connect('/root/nagios.db')       # 디비 설정
        c = conn.cursor()

        if 0 < len(G):                                  # wUpdate 인자로 받은 리스트내 값들의 수가 0보다 클 경우, 즉 리스트내에 값이 있을경우
            for item in G:
                item = item.replace(" ","")             # HostName 의 공백제거
                c.execute(real_query % item)            # HostName 명을 가진 테이블 확인 (0 = 없음, 1 = 있음)
                r = c.fetchone()
                if 0 == r[0]:                           # 튜플로 받아온 값 판별하여 (0) 테이블이 없을 경우
                    c.execute(create_query % item)      # 테이블 생성
                    c.execute(insert_w_query % item)    # 테이블 생성 후 데이터 입력
                    conn.commit()                       # COMMIT
                else:
                    c.execute(insert_w_query % item)    # 튜플로 받아온 값 (1) 테이블이 있을 경우 그대로 데이터 입력
                    conn.commit()                       # COMMIT
        else:                                           # wUpdate 인자로 받은 리스트내 값들의 수가 0일 경우, 즉 리스트내에 값이 없을 경우
            tablelist = list(c.execute(table_query))    # 현재 디비내에 있는 모든 테이블명 조회
            for table in tablelist:
                c.execute(null_query % table)           # 테이블마다 Null 값 데이터 입력(sms 발송여부 판단 위해 마지막 데이터 값을 판단하므로)
                conn.commit()

        conn.close()

    def cUpdate(self, G):                               # Critical Update
        conn = sqlite3.connect('/root/nagios.db')       # 디비 설정
        c = conn.cursor()

        if 0 < len(G):                                  # wUpdate 인자로 받은 리스트내 값들의 수가 0보다 클 경우, 즉 리스트내에 값이 있을경우
            for item in G:
                item = item.replace(" ","")             # HostName 의 공백제거
                c.execute(real_query % item)            # HostName 명을 가진 테이블 확인 (0 = 없음, 1 = 있음)
                r = c.fetchone()
                if 0 == r[0]:                           # 튜플로 받아온 값 판별하여 (0) 테이블이 없을 경우
                    c.execute(create_query % item)      # 테이블 생성
                    c.execute(insert_c_query % item)    # 테이블 생성 후 데이터 입력
                    conn.commit()                       # COMMIT
                else:
                    c.execute(insert_w_query % item)    # 튜플로 받아온 값 (1) 테이블이 있을 경우 그대로 데이터 입력
                    conn.commit()                       # COMMIT
        else:                                           # wUpdate 인자로 받은 리스트내 값들의 수가 0일 경우, 즉 리스트내에 값이 없을 경우
            tablelist = list(c.execute(table_query))    # 현재 디비내에 있는 모든 테이블명 조회
            for table in tablelist:
                c.execute(null_query % table)           # 테이블마다 Null 값 데이터 입력(sms 발송여부 판단 위해 마지막 데이터 값을 판단하므로)
                conn.commit()

        conn.close()
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

#################
#               #
#    Process    #
#               #
#################

# Parsing JSON from status.dat
nagiStat = subprocess.check_output(['nagios-status-parser /usr/local/nagios/var/status.dat'], shell=True)
nagiPar = json.loads(nagiStat)

# Export list
e = nagiosStatParsing()
W = e.WAR()
C = e.CRI()

# Check status
e2 = sqlitedb()
e2.wUpdate(W)
e2.wUpdate(C)