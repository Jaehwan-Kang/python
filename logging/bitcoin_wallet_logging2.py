#!/usr/bin/python
# -*- coding:utf-8 -*-
import bitcoinrpc, datetime, sys, pymysql, redis, json

_backupPath = "/CHAIN_BITCOIN/"
_logPath = "/CHAIN_BITCOIN/"
_walletLogData = sys.argv[1]


date = datetime.datetime.now()
_nowDate = date.strftime("%Y%m%d-%H:%M:%S")
_logDate = date.strftime("%Y%m%d")

_logFile = "%swallet_log-%s" % (_logPath, _logDate)
_backWalletfile = "%s%s-wallet.dat" % (_backupPath, _nowDate)

_tranFile = "%stran_log" % _logPath

# Wallet Logging
with open(_logFile, 'a') as f:
    f.write("%s ==== %s\n" % (_nowDate, _walletLogData))

conn = bitcoinrpc.connect_to_local()
_tranData = json.loads(conn.gettransaction(sys.argv[1]))

with open(_tranFile, 'a') as f:
    f.write(_tranData)


# 8e83d0fd40c1ae951285c76bf2d854fa85024f227bb123c3081e935846d0a4b9
# 9896f9086d73f1007300cae5eb84fd1657d1659f75770d075e693dfce43b33af
# 723b041dd535745bf1888bc51af2e13aad195cfe51adc98d4e7b4722fa755073

# # Wallet Backup
# try:
#     conn = bitcoinrpc.connect_to_local()
#     conn.backupwallet(_backWalletfile)
# except:
#     with open(_logFile, 'a') as f:
#         f.write("%s ==== Wallet Backup Failed\n" % _nowDate)

# Transaction Info Collect

# db = pymysql.connect(host='192.168.10.92', port=3306, user='root', passwd='1234', db='transaction_log', charset='utf8', autocommit=True)
#
# cursor = db.cursor()
# try:
#     sql = 'INSERT INTO bitcoin2 (bl_txid, bl_transaction_reg_data, bl_transaction_alted_data, bl_reg_date) VALUES (%s, %s, '{""}', NOW())'
#     cursor.execute(sql, (sys.argv[1], _Tdata))
# except:
#     with open(_logFile, 'a') as f:
#         f.write("%s ==== DB Insert Failed\n" % _nowDate)
#
# db.close()


#r = redis.Redis(host='192.168.10.92', port=6379)

데이터센터  [Seoul 1]
그룹계정 : test909090
가상서버 : B1.1x2x25  2대 
네트워크 : Load Balancer 250 VIP Connections 

