#!/bin/bash

path=$1
target=$2
cd $path

cloc --sum-one $path$target > LOC.txt