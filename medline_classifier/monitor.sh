#!/bin/bash

pid=$1

while true; do
    stats=`ps -p $pid -o %cpu,%mem,cmd`
    echo $stats
    echo $stats >> stats.log
    sleep 1m
done
