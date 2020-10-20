#!/bin/bash

path=$1
hash=$2
currentpath=${PWD}
now=$(date)
echo -e $now: BEGIN git checkout: $hash \\n 

cd $path

git checkout $hash

now=$(date)

echo -e $now: END git checkout \\n 
