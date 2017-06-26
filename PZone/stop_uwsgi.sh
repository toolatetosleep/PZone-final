#!/bin/sh
NAME="PZone"
if [ ! -n "$NAME" ];then
    echo "no arguments"
    exit;
fi

echo "Stoping "$NAME
# echo "PID:"
ID=`ps -ef | grep "$NAME" | grep -v "$0" | grep -v "grep" | awk '{print $2}'`
# echo $ID
# echo "Killin'.."
for id in $ID
do
kill -9 $id
echo "kill $id"
done
echo $NAME" is stoped."
