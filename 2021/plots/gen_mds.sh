#!/bin/bash
WEBROOT=../../../smt-comp.github.io/

#./plot.sh -c -s

(
    echo "---"
    echo "figures:"
    ls figures/*.yml \
        | while read -r file; do
            echo "Processing $file" > /dev/stderr
            bname=$(basename "$file" .yml)
            echo "- $bname:"
            sed -e 's/^/  /' "$file"
            cp "figures/$bname.svg" $WEBROOT/2021/par-cloud-analysis/"$bname.svg"
        done

    echo "---"
    cat content/description.md

) > $WEBROOT/2021/parallel-and-cloud-tracks.md

