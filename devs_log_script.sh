#!/bin/bash

path=$1
currentpath=${PWD}
now=$(date)
echo -e $now: BEGIN git devs count: $path \\n 

cd $path

git config diff.renameLimit 999999 

#Extract commit information
git log | grep Author: | sort | uniq > devsinfo.log

git config --unset diff.renameLimit


now=$(date)
echo -e "Log files (devsinfo.log) were generated in $path folder:  \\n"
echo -e $now: END git devs count: $path \\n 
