#!/bin/bash

## android 8.0.0  samsung
cd /sys/devices/virtual/thermal

idx=0
count=0
total=0
while [ -d thermal_zone${idx} ]; do
    type=`cat thermal_zone${idx}/type`

    # huawei
    if [ type == "soc_thermal"]; then
        temp=`cat thermal_zone${idx}/temp`
        total=total+$((temp))
        count=count+1
    fi
done

temp=$((total/count))
echo "temp is $temp"

