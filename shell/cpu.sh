#!/bin/bash

xentop -d1 -b -f > cpu-util-detail.log

cat cpu-util-detail.log | awk '/Cloud_Gaming*/ {print $1,$4}' > cpu-util-short.log

echo -e "\nVM-Name \t CPU-Util(%)\n"
cat cpu-util-short.log
