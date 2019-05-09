#!/usr/bin/env bash


virten

make devserver PORT=3543

sleep 30; 

make rmindex;

echo "OK? upload to github? [N/n]";

read next

if [[ $next == "Y" || $next == "y" ]]
then
    cd output
    git add .
    git status
    echo "input the message"
    
    read mes
    git commit -m "$mes"
    gpush
fi