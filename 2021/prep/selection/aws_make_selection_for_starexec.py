#!/bin/bash

SCRIPTDIR=$(cd $(dirname $0); pwd)
csvcut -c 'smtlib name' ${SCRIPTDIR}/final/parallel-map.csv |tail +2 > ${SCRIPTDIR}/final/benchmark_selection_parallel_starexec
csvcut -c 'smtlib name' ${SCRIPTDIR}/final/cloud-map.csv |tail +2 > ${SCRIPTDIR}/final/benchmark_selection_cloud_starexec
