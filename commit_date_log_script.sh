#!/bin/bash

path=$1
currentpath=${PWD}
now=$(date)
echo -e $now: BEGIN git log extraction: $path \\n 

cd $path

git config diff.renameLimit 999999 


#Extract commit information
git log --pretty=format:"%H,%at"  > /home/brenner/MSI/data/log.csv

git config --unset diff.renameLimit

now=$(date)
echo -e $now: END git log extraction: $path \\n 
