#!/usr/bin/env bash
for dir in ./$1/*
do
    echo $dir
    files="concat:"
    for file in $dir/*
    do
        files+=$file
        files+="|"
    done
    idx=$(echo $dir | cut -d/ -f 4)
    session_id=$(echo $dir | cut -d/ -f 3)
    output_name=$session_id'_'$idx
    ffmpeg -i $files -c copy static/videos/$output_name.mp4 2> /dev/null
done


