#!/bin/bash

function matchResultExpected {
    file=$1
    result=$2
    expected=$3
    cat $file \
        |csvcut -c 'solver id,benchmark,result,expected' \
        |csvgrep -c result -r "^$result\$" \
        |csvgrep -c expected -r "^$expected\$" \
        |csvcut -c 'solver id,benchmark' \
        |sed 's!^\([^,]*\),[^/]*/\([^/]*\)/.*!\1,\2!g' \
        |tail +2 \
        |sort \
        |uniq
}

if [ $# != 2 ]; then
    echo "usage: $0 <result-file> <id-to-name-map>"
    exit 1
fi

(
    echo "solver id,logic";
    matchResultExpected $1 'sat' 'unsat';
    matchResultExpected $1 'unsat' 'sat';
) |csvjoin -c 'solver id,solver id' /dev/stdin $2

