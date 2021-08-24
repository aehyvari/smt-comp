#!/bin/bash

Cloud="cloud"
Parallel="parallel"

smtlib_root=$1

for track in Cloud Parallel; do
    ./aws_fetch.sh $track ${!track} $smtlib_root
done

