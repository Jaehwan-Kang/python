#!/usr/bin/env bash
#
#
#  Usage #check_haproxy_stat.sh [pxname] [svname] [haproxyserver URL or IP] [Auth info]
#
#  ex) ./check_haproxy_stat.sh sumradio_http web3 "http://211.61.155.151:1936" "cyebiz:Cyebizadmin151"
#

_Checkpxname=$1
_Checksvname=$2
_HaproxyServer=$3
_HaproxystatAUTH=$4
_HaproyCSV="/usr/local/nagios/var/haproxy.stat"

if [ $# = 4 ]
        then
        /usr/bin/curl --user $_HaproxystatAUTH "$_HaproxyServer/;csv" > $_HaproyCSV 2>>/dev/null
        STAT=`/usr/bin/grep "$_Checkpxname" $_HaproyCSV | /usr/bin/grep "$_Checksvname" | head -1 | awk -F, '{print $37}'`

        if [ "$STAT" = "L7OK" -o "$STAT" = "L6OK" ]
                then
                echo "$STAT =  $_Checkpxname [$_Checksvname]"
                exit 0;

                else
                        echo "Critical = You need check service  $_Checkpxname [$_Checksvname]"
                        exit 2;
        fi

        else
                echo "Error>> Argument is Not Match!"
                exit 1;

fi