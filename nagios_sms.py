#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#   Nagios_sms.py  - kang.jh@cyebiz.com
#
#   Nagios  : status.dat
#   SQLite3 : /root/nagios.db
#   SMS     : sms.cyebiz.com
#
#  [Ready]
#   prompt>> yum -y install npm python python-pip
#   prompt>> npm install -g nagios-status-parser
#   prompt>> pip install subprocess requests sqlite3
#   prompt>> nagios-status-parser /usr/local/nagios/var/status.dat
#
#  [Example]
#   /etc/crontab
#   # 5분마다 실행
#   */5 * * * * root /root/nagios_sms.py
#


import json, subprocess, requests, sqlite3              # Load Modules

##########################
#                        #
#  Check Nagios Statlist #
#                        #
##########################

class nagiosStatParsing:                                # nagiosStatParsing 클래스

    def sorting(self):                                  # sortiung 함수
        global nagiPar                                  # 글로벌 변수
        statlist = {}                                   # statlist 딕셔너리 초기화
        for item in nagiPar["servicestatus"]:
            if 1 == item["current_state"]:              # 상태 1(warning) 일 경우  "이름":"상태" 딕셔너리 값 입력
                statlist[item["host_name"]] = item["current_state"]
            elif 2 == item["current_state"]:            # 상태 2(critical) 일 경우  "이름":"상태" 딕셔너리 값 입력
                statlist[item["host_name"]] = item["current_state"]
        return statlist

#################
#               #
#    Sqlite3    #
#               #
#################

real_query = "select count(*) from sqlite_master Where Name = '%s'"
create_query = "create table %s (No INTEGER PRIMARY KEY AUTOINCREMENT, State_code varchar (10), Date datetime default (datetime('now','localtime')))"
insert_w_query = "insert into %s (State_code) values ('1')"
insert_c_query = "insert into %s (State_code) values ('2')"
table_query = "SELECT name FROM sqlite_master WHERE type IN ('table', 'view') AND name NOT LIKE 'sqlite_%' UNION ALL SELECT name FROM sqlite_temp_master WHERE type IN ('table', 'view') ORDER BY 1"
null_query = "insert into %s (State_code) values('');"
select_query = "select State_code from %s order by Date desc limit 0,1;"

class sqlitedb:                                         # sqlitedb 클래스

    def Update(self, Hosts):                            # Update 함수
        conn = sqlite3.connect('/root/nagios.db')       # 디비 설정
        c = conn.cursor()

        if 0 < len(Hosts):                              # Update 인자로 받은 리스트내 값들의 수가 0보다 클 경우, 즉 리스트내에 값이 있을경우

            for name, item in Hosts.items():
                name = name.replace(" ","")             # HostName 의 공백제거

                if 1 == item:                           # Hosts DIC의 item = 1 일 경우 insert_w_query 사용
                    query = insert_w_query
                elif 2 == item:                         # Hosts DIC의 item = 2 일 경우 insert_c_query 사용
                    query = insert_c_query

                c.execute(real_query % name)            # HostName 명을 가진 테이블 확인 (0 = 없음, 1 = 있음)
                r = c.fetchone()

                if 0 == r[0]:                           # 튜플로 받아온 값 판별하여 (0) 테이블이 없을 경우
                    c.execute(create_query % name)      # 테이블 생성
                    c.execute(query % name)             # 테이블 생성 후 데이터 입력
                    conn.commit()                       # COMMIT
                else:
                    c.execute(query % name)             # 튜플로 받아온 값 (1) 테이블이 있을 경우 그대로 데이터 입력
                    conn.commit()                       # COMMIT

                                                        # !!!! 바로 위에서 insert 쿼리가 실행된 후에 아래가 진행되야함 !!!!!
            c.execute(table_query)                      # 현재 디비내에 있는 모든 테이블명 조회
            tablelist = c.fetchall()                    # 조회된 값을 list 로 변경 **주의 : list이나 값들은 tuple!!!!!

            updatetablelist = []                        # updatetablelist 초기화
            for x in tablelist:                         # (A-0)조회된 전체 테이블 목록은 tuple 형태로 이를 list로 변환
                x = str(x)
                updatetablelist.append(x)

            for name in Hosts.keys():
                name = name.replace(" ","")
                name2 = "(u\'%s\',)" % name             # (A-1)
                I = updatetablelist.index(name2)        # (A-1) list 로 변환된 테이블명에서 이벤트발생된 HostName 제외
                del updatetablelist[I]                  # (A-1) 이벤트 발생된 HostName 삭제

            for table in updatetablelist:               # (A-2) (A-1) 에서 갱신된 updatetablelist 이용
                table = table.replace("(u\'","")
                table = table.replace("\',)","")
                c.execute(null_query % table)           # (A-2)갱신된 테이블목록으로 각각 Null 값 데이터 입력(sms 발송여부 판단 위해 마지막 데이터 값을 판단하므로)
                conn.commit()                           # COMMIT

        else:                                           # Update 인자로 받은 리스트내 값들의 수가 0, 0보다 작을 경우, 즉 리스트내에 값이 없을경우

            for table in tablelist:
                c.execute(null_query % table)           # 모든 테이블에 Null 값 데이터 입력(sms 발송여부 판단 위해 마지막 데이터 값을 판단하므로)
                conn.commit()                           # COMMIT

        conn.close()

    def Check(self, Hosts):
        conn = sqlite3.connect('/root/nagios.db')       # 디비 설정
        c = conn.cursor()
        c.execute(table_query)                          # 현재 디비내에 있는 모든 테이블명 조회
        tablelist = c.fetchall()                        # 조회된 값을 list 로 변경 **주의 : list이나 값들은 tuple!!!!!

        now_list = []                                   # 현재 event 발생된 현재 Hosts 들의 list 자료화
        for x in Hosts.keys():                          # 공백 제거 후 list 자료화
            x = x.replace(" ","")
            now_list.append(x)

        last_list = []                                  # nagios.db 내 모든테이블 select 하여 마지막 체크때 state_code를 가진 list 자료화위한 초기화

        for table in tablelist:                         # 조회된 모든 테이블 명에 대하여 마지막 체크때 State_Code 값 조회
            c.execute(select_query % table)
            r = c.fetchone()

            table = str(table)

            if "" != r[0]:                              # 마지막 체크때 State_code 값이 있을경우,
                table = table.replace("(u\'","")        # 문자열 가공
                table = table.replace("\',)","")        # 문자열 가공
                last_list.append(table)                 # last_list 에 LIST UP
        conn.close()

        s1 = set(now_list)                              # 현재 event 발생된 host 리스트
        s2 = set(last_list)                             # 디비 내 마지막(5분전) 에 event가 있었던 host 리스트
        s3 = s1 & s2                                    # 위의 2개 리스트의 교집합. 중복된.  즉, 10분간 event 가 발생된 것으로 간주된 Host 확인
        result = len(s3)                                # 10분간 event 발생된 Host의 수량 return
        return result


##############
#            #
#  Send SMS  #
#            #
##############

# GET 요청시
# http://sms.cyebiz.com/sms_send.php?type=sms&name=%EC%A1%B0%EC%97%B0%ED%98%B8&phone=01028241085&msg=TEST%20MESSAGE&callback=0263423352&apiKey=8a1b076d4da59d51eac3d59a2903c744


def SendSMS(phone, nagiosMessage):
    phone_number = phone

    NagiosMSG = nagiosMessage

    url = 'http://sms.cyebiz.com/sms_send.php'

    headers = {
        'user-agent': 'CYEBIZ/1.0'
    }
    postdata = {
        'type':'sms',
        'returnurl':'',
        'reserve':'0',
        'name':'Nagios',
        'phone': phone_number,
        'msg': NagiosMSG,
        'callback':'0263423352',
        'apikey':'8a1b076d4da59d51eac3d59a2903c744',
        'etc1':'',
        'etc2':'',
        'timeout':'3'
    }
    r = requests.post(url, headers=headers, data=postdata)

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
E = e.sorting()

# Check status
e2 = sqlitedb()
event = e2.Check(E)

# DB Update
e2.Update(E)

# Event SMS Sending
recv_phone = "01028241085"
if 0 < event:
    msg = "Event Hosts : %s" % event
    SendSMS(recv_phone, msg)