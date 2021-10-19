#!/bin/bash
WEBROOT=../../../smt-comp.github.io/

#./plot.sh -c -s

mkdir -p $WEBROOT/_plots_2021
mkdir -p $WEBROOT/2021/plot_data

cp content/description.md $WEBROOT/2021/parallel-and-cloud-tracks.md
cp content/plot_summary.html $WEBROOT/2021/plot_summary.html
cp content/plot_scatter.html $WEBROOT/2021/plot_scatter.html
cp content/plot_cactus.html $WEBROOT/2021/plot_cactus.html
cp figures/*.md $WEBROOT/_plots_2021/
cp figures/*.svg $WEBROOT/2021/plot_data

