#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# - 서버별 파일 리스트 출력
#
# - 서버별 파일크기 합계 출력

import json
from collections import OrderedDict


# 맨 윗 라인 제거
_Target = "/Users/jaehwankang/Documents/Develop/Python/list.txt"
_Return = "/Users/jaehwankang/Documents/Develop/Python/newlist.txt"

list = open(_Target).readlines()
open(_Return, 'w').writelines(list[1:])


# 데이터 파싱
with open(_Return, 'r') as parsing:
    server_list = []

    ## 유니크 서버 리스트 추출
    for line in parsing:
        item = line.split(",")
        server = item[4].split(" ")
        for i in server:
            server_list.append(i)
        # 전체 서버 리스트 (약 158000여 개수)의 중복을 제거 / set 이용시 오류 발생
        server_list = dict().fromkeys(server_list).keys()

with open(_Return, 'r') as parsing:

    for line in parsing:
        item = line.split(",")
        server = item[4].split(" ")


        if server[0] in server_list:
            print("{'Server': '%s', 'FileName': '%s', 'FileSize': %s}" % (server[0],item[0],item[3]))

        if server[1] in server_list:
            print("{'Server': '%s', 'FileName': '%s', 'FileSize': %s}" % (server[0], item[0], item[3]))

                #for i in server_list:
        #print(i)

# Ready for data
group_data = OrderedDict()
#albums = OrderedDict()

group_data["name"] = "Server_List"
group_data["svr_members"] = server_list

#albums["EP 1집"] = "Season of Glass"
#albums["EP 2집"] = "Flower Bud"
#albums["EP 3집"] = "Snowflake"
#albums["정규 1집"] = "LOL"
#albums["EP 4집"] = "THE AWAKENING"

#group_data["albums"] = albums

# Print JSON
#print(json.dumps(group_data, ensure_ascii=False, indent="\t"))

{
    "members": {

        "서버IP": {
            "파일명":"파일크기",
            },

        "서버IP": {
           "파일명":"파일크기",
        },

    }

}





#파일명 , 파일 생성시간, 비트레이트, 파일 크기, 파일 존재 하는 서버,
