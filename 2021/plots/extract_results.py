#!/usr/bin/env python3

import csv
from argparse import ArgumentParser, BooleanOptionalAction
import json
import sys

# Default track for division extraction
TRACK_DEFAULT = "track_single_query"

# StarExec result strings
RESULT_UNKNOWN = 'starexec-unknown'
RESULT_SAT = 'sat'
RESULT_UNSAT = 'unsat'
RESULT_UNSOUND = 'unsound'

def die(s):
    print(s)
    sys.exit(1)

def isSound(result, expected):
    if result == RESULT_SAT and expected == RESULT_UNSAT:
        return False
    if result == RESULT_UNSAT and expected == RESULT_SAT:
        return False
    return True

def stripJobName(benchmark):
    return benchmark[benchmark.find('/'):]

def normalise(result):
    return result if not result == RESULT_UNKNOWN else 'indet'

def readResultsCsv(csvname, solver, timeout):
    res = dict()
    with open(csvname) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['solver id'] != solver:
                continue

            if isSound(row['result'], row['expected']):
                result = row['result']
            else:
                result = RESULT_UNSOUND

            time = float(row['wallclock time'])

            name = stripJobName(row['benchmark'])

            res[name] = { 'result': normalise(result), 'time': time}

    return res

def parseArgs():
    parser = ArgumentParser()
    parser.add_argument("-c", "--csv", required=True, help="Results csv file from StarExec")
    parser.add_argument("-s", "--solver", required=True, help="Solver name")
    parser.add_argument("-t", "--timeout", required=True, \
            help="Timeout for the experiment")
    parser.add_argument("-d", "--division", required=False, \
            help="Division from which to extract the results")
    parser.add_argument("-f", "--file", required=False, \
            help="Division file")
    parser.add_argument("-r", "--track", required=False, \
            help="A track from the division file")
    parser.add_argument("-o", "--output", default=True, \
            action=BooleanOptionalAction, \
            help="produce the output.  If false, do not produce a list "\
            "of results, but instead exit with zero iff a result list "\
            "would have been non-empty")
    return parser.parse_args()

def main():
    args = parseArgs()
    results = readResultsCsv(args.csv, args.solver, float(args.timeout))
    if args.division:
        division = args.division
        if not args.file:
            die("ERROR: division specified but no division file provided")
        tracks = json.loads(open(args.file).read())
        if not args.track:
            print("No track provided.  Using `{}`".format(TRACK_DEFAULT))
            track = TRACK_DEFAULT
        else:
            track = args.track

        if track not in tracks:
            die("{} not in tracks".format(track))

        divisions = tracks[track]
        if division not in divisions:
            die("{} not in divisions".format(division))

        logics = divisions[division]

        results_tmp = dict()
        for k in results:
            if k.split("/")[1] in logics:
                results_tmp[k] = results[k]

        results = results_tmp

    if args.output:
        for k in sorted(list(results), key=lambda x: results[x]['time']):
            print("{} {} {}".format(k, results[k]['result'], results[k]['time']))
    sys.exit(0 if len(results) > 0 else 1)


if __name__ == "__main__":
    main()

