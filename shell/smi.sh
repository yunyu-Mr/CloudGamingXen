#!/bin/bash

#Program:
#        nvidia-smi tool
#
#        -q: query
#        -d: display utilization
#        -i: info, choose the first one
#        -l: loop, log file for every 10 sec
#        -f: filename, log file

#Author: Saoming

#History: 2015/06/16

nvidia-smi -q -d UTILIZATION -i 0 -l 10 -f smi-util.log

# xentop -d1 -b -f | awk '/Cloud_Gaming*/ {print $1,$4}'

# Display all lines that contain keyword 'Gpu'. Using awk tool.
cat smi-util.log |awk '/Gpu/ {print}' > gpu-util.log
cat gpu-util.log
