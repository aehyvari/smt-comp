#!/usr/bin/env python3

import csv
import sys
import argparse
import os
import yaml

# Change the timeout here if needed
to = 1200

usage = """
Create scatter plot gnuplot scripts using a png driver.  The results
files should consist of lines of the form

<name> <result> <time>

where <name> identifies uniquely a formula, <result> is
indet, sat, unsat, or unsound and <time> is a
floating point number.
"""

def getSolverIdMap(f):

    SOLVER_ID_COLUMN = "solver id"
    SOLVER_NAME_COLUMN = "solver name"

    res = dict()
    with open(f) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            res[row[SOLVER_NAME_COLUMN]] = row[SOLVER_ID_COLUMN]
    return res

def parseArgs():
    parser = argparse.ArgumentParser(description=usage)
    parser.add_argument("track", help="the track of the result")
    parser.add_argument("xresults", help="results for x-axis")
    parser.add_argument("yresults", help="results for y-axis")
    parser.add_argument("xlabel", help="label for x-axis")
    parser.add_argument("ylabel", help="label for y-axis")
    parser.add_argument("output", help="output file name (png)")

    return parser.parse_args()

if __name__ == '__main__':

    args = parseArgs()

    output = args.output
    xlabel = args.xlabel
    ylabel = args.ylabel

    description_name = os.path.splitext(output)[0]

    description = dict()
    description['name'] = os.path.basename(description_name)
    description['track'] = args.track
    description['type'] = "scatter"
    description['x-axis'] = xlabel
    description['y-axis'] = ylabel

    x_l = open(args.xresults, 'r').readlines()
    y_l = open(args.yresults, 'r').readlines()


    use_log = True

    def getRes(lst):
        h_out = {}
        for el in lst:
            rec = el.split()
            name = rec[0]
            res = rec[1]
            time = -1
            if len(rec) > 2:
                time = rec[2]
            if name in h_out:
                print("Duplicate result: %s" % name)
                sys.exit(1)
            if (res == 'indet') and float(time) < to:
                time = -2 # mem out
            elif (res == 'indet'):
                time = -1 # time out
            elif (res == 'unsound'):
                time = -3 # unsound
            h_out[name] = [res, float(time)]
        return h_out

    try:
        x_res = getRes(x_l)
        y_res = getRes(y_l)
    except UnboundLocalError as e:
        print(e)
        print("Problem: %s, %s" % (x_l, y_l))
        sys.exit(1)
    try:
        max_x = max(map(lambda x: x_res[x][1], x_res))
        min_x = min(filter(lambda x: x >= 0, \
                map(lambda x: x_res[x][1], x_res)))
    except ValueError as e:
        print("No results for {}".format(xlabel))
        sys.exit(1)
    try:
        max_y = max(map(lambda x: y_res[x][1], y_res))
        min_y = min(filter(lambda x: x >= 0, \
                map(lambda x: y_res[x][1], y_res)))
    except ValueError as e:
        print("No results for {}".format(ylabel))
        sys.exit(1)

    max_all = max(max_x, max_y)

    low = min(min_x, min_y)

    if (use_log):
        bnd = 1.5*to
        bnd2 = 2*to
        bnd3 = 2.5*to
    else:
        bnd = 1.01*to
        bnd2 = 1.02*to
        bnd3 = 1.03*to

    speedups = []
    x_total = 0
    y_total = 0

    for k in x_res.keys():
        if (k in y_res and x_res[k][1] >= 0 and y_res[k][1] > 0):
            speedups.append(x_res[k][1]/float(y_res[k][1]))
            x_total += float(x_res[k][1])
            y_total += float(y_res[k][1])
        elif k not in y_res:
            print("Not in y: %s" % k, file=sys.stderr)

    for k in y_res.keys():
        if k not in x_res:
            print("Not in x: %s" % k, file=sys.stderr)

    speedup = sum(speedups)/len(speedups)

    description['average_speedup'] = speedup
    description['total_speedup'] = x_total/float(y_total)

    solved_x = len(list(filter(lambda x: x_res[x][1] >= 0, x_res.keys())))
    solved_y = len(list(filter(lambda x: y_res[x][1] >= 0, y_res.keys())))
    print("x solved: {}, y solved: {}".format(solved_x, solved_y), file=sys.stderr)

    description['x-solved'] = solved_x
    description['y-solved'] = solved_y

    def postProc(h):
        for k in h:
            if h[k][1] == -1:
                h[k][1] = bnd
            elif h[k][1] == -2:
                h[k][1] = bnd2
            elif h[k][1] == -3:
                h[k][1] = bnd3

    postProc(x_res)
    postProc(y_res)

    print('#!/usr/bin/env gnuplot')
    print('set term svg dynamic font "Arvo"')

    print('set output "%s"' % output)
    print('set size square')
    print('set size 0.8, 0.8')
    print('set xlabel "%s"' % xlabel)
    print('set ylabel "%s"' % ylabel)
    if (use_log):
        print('set logscale x')
        print('set logscale y')
    print('set key right bottom')
    print('set xrange [%f:%f]' % (low, bnd3))
    print('set yrange [%f:%f]' % (low, bnd3))
    print('set pointsize 1.5')
    for b in (to, bnd, bnd2):
        print('set arrow from graph 0, first %f to %f,%f nohead' % (b, b, b))
        print('set arrow from %f, graph 0 to %f,%f nohead' % (b, b, b))

    print('set arrow from %f, graph 0 to graph .98, graph -.07 backhead lt 2' % bnd)
    print('set label "t/o" at graph .95, graph -0.1')
    print('set arrow from %f, graph 0 to graph 1.05, graph -.04 backhead lt 2' % bnd2)
    print('set label "m/o" at graph 1.05, graph -0.06')
    print('set arrow from %f, graph 0 to graph 1.1, graph -.02 backhead lt 2' % bnd3)
    print('set label "unsound" at graph 1.1, graph -0.00')

    print('set label "sp %.02f" at graph 1.01,1.0' % speedup)
    print('set label "sp tot %.02f" at graph 1.01,0.9' % (x_total/float(y_total)))
    print('set label "solved x %d" at graph 1.02,0.8' % solved_x)
    print('set label "solved y %d" at graph 1.02,0.7' % solved_y)
    print('plot x title "" lc "black", '\
            '"-" title "" with point pointtype 2 lc "black", '\
            '"-" title "" with points pointtype 4 lc "black", '\
            '"-" title "" with points pointtype 3 lc "black", '\
            '"-" title "" with points pointtype 5 lc 1, '\
            '"-" title "" with points pointtype 5 lc 2')

    sat_strings = []
    unsat_strings = []
    ukn_strings = []
    fail_strings = []
    unsound_strings = []
    for name in x_res:
        if name in y_res:
            if (x_res[name][0] == 'sat' and \
                y_res[name][0] == 'unsat') or \
               (x_res[name][0] == 'unsat' and \
                y_res[name][0] == 'sat'):
                print("Oops: %s %s %s" %
                        (name, x_res[name], y_res[name]), file=sys.stderr)
                fail_strings.append("%.02f %.02f # %s" % (x_res[name][1], y_res[name][1], name))

            elif (x_res[name][0] == 'sat') or (y_res[name][0] == 'sat'):
                sat_strings.append("%.02f %.02f # %s" % (x_res[name][1], y_res[name][1], name))
            elif (x_res[name][0] == 'unsat') or (y_res[name][0] == 'unsat'):
                unsat_strings.append("%.02f %.02f # %s" % (x_res[name][1], y_res[name][1], name))
            elif (x_res[name][0] == 'unsound') or (y_res[name][0] == 'unsound'):
                unsound_strings.append("%0sf %.02f # %s" % (x_res[name][1], y_res[name][1], name))
                if 'unsound' not in description:
                    description['unsound'] = []
                if x_res[name][0] == 'unsound':
                    description['unsound'].append(\
                            {'instance': name, 'solver': xlabel})
                if y_res[name][0] == 'unsound':
                    description['unsound'].append(\
                            {'instance': name, 'solver': ylabel})
            else:
                ukn_strings.append("%.02f %.02f # %s" % (x_res[name][1], y_res[name][1], name))

    print("\n".join(sat_strings))
    print("e")
    print("\n".join(unsat_strings))
    print("e")
    print("\n".join(ukn_strings))
    print("e")
    print("\n".join(fail_strings))
    print("e")
    print("\n".join(unsound_strings))
    print("e")

    descr_file = open("{}.yml".format(description_name), 'w')
    descr_file.write(yaml.dump(description))

