#!/bin/sh

#sed '1d' list.txt > temp.txt

for i in `cat temp.txt`
	do
	name=`awk -F, '{print $1}' $i`
	#server1=`awk -F, '{print $5}' $i|awk '{print $1}'` 
	#server2=`awk -F, '{print $5}' $i|awk '{print $2}'` 
	
	echo $name $server1 $server2
	done
