#!/usr/bin/env python3

import csv
from argparse import ArgumentParser, BooleanOptionalAction

import sys

TRACK_TO_COLUMN = {
        'track_single_query': 'Wrapped Solver ID Single Query',
        'track_incremental': 'Wrapped Solver ID Incremental',
        'track_model_validation': 'Wrapped Solver ID Model Validation',
        'track_unsat_core': 'Wrapped Solver ID Unsat Core',
        'track_cloud': 'Solver ID',
        'track_parallel': 'Solver ID'
        }

NAME_COLUMN = 'Solver Name'

def die(msg):
    print(msg)
    sys.exit(1)

def getSolverIds(csvname):
    res = dict()
    with open(csvname) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sq_id = row[TRACK_TO_COLUMN['track_single_query']]
            parallel_id = row[TRACK_TO_COLUMN['track_cloud']]
            id = sq_id if sq_id != "" else parallel_id
            res[id] = row[NAME_COLUMN]

    return res

def parseArgs():
    parser = ArgumentParser()
    parser.add_argument("-c", "--csv", required=True, \
            help = "The registration CSV file")
    return parser.parse_args()

def main():
    args = parseArgs()

    names = getSolverIds(args.csv)
    print("solver name,solver id")
    for k in names:
        print('"{}",{}'.format(names[k], k))

if __name__ == '__main__':
    main()
