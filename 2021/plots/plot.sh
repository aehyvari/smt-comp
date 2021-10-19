#!/bin/bash

RESULTS=../scoring/
PLOTTER=./make_scatterplot_time.py
CACTUSPLOTTER=./make_cactusplot_time.py
EXTRACTOR=./extract_results.py
DIVISION_FILE=../new-divisions.json
SOLVERS_CSV=../registration/solvers_divisions_final.csv

export LC_CTYPE=C


function getSolverId() {
    solver=$1
    cat $tmpdir/idToNameMap.csv \
    | csvgrep -c 'solver name' -r "^$solver\$" \
    | csvcut -c 'solver id' \
    | tail +2 | head
}

function getSolverName() {
    solver_id=$1
    cat $tmpdir/idToNameMap.csv \
    | csvgrep -c 'solver id' -r "^$solver_id\$" \
    | csvcut -c 'solver name' \
    | tail +2 | head
}

function compare() {
    echo "Comparing between $1 and $2 in $3"
    solver_id_1=$(getSolverId "$1")
    solver_id_2=$(getSolverId "$2")

    $EXTRACTOR --solver "$solver_id_1" \
        --csv $RESULTS/results-$3.csv \
        --timeout 1200 \
        > $tmpdir/"$1"-$3.list

    $EXTRACTOR --solver "$solver_id_2" \
        --csv $RESULTS/results-$3.csv \
        --timeout 1200 \
        > $tmpdir/"$2"-$3.list

    $PLOTTER \
        $3 \
        $tmpdir/"$1"-$3.list \
        $tmpdir/"$2"-$3.list \
        "$1" \
        "$2" \
        figures/"$1"_vs_"$2"_$3.svg \
        2021 \
        > figures/"$1"_vs_"$2"_$3.gp \

    gnuplot figures/"$1"_vs_"$2"_$3.gp
}

function createCactusList() {
    if [ $1 == "sq" ]; then
        track_tmp="single_query"
    else
        track_tmp=$1
    fi
    solver_id=$2
    division=$3
    solver=$(getSolverName "$solver_id")

    outname=$tmpdir/"$solver".list

    rm -rf $outname

    if $($EXTRACTOR -c $RESULTS/results-$1.csv \
            -s "$solver_id" \
            -t 1200 \
            -d "$division" \
            --track "track_$track_tmp" \
            -f $DIVISION_FILE \
            --no-output); then

        echo "$outname"
        $EXTRACTOR -c $RESULTS/results-$1.csv \
            -s "$solver_id" \
            -t 1200 \
            -d "$division" \
            --track "track_$track_tmp" \
            -f $DIVISION_FILE \
            > "$outname"
    fi
}

function getDivisionNames() {
    if [ $1 == "sq" ]; then
        track=single_query
    else
        track=$1
    fi
    python3 << __EOF__
import json
print(" ".join(json.loads(open("$DIVISION_FILE", "r").read())["track_$track"].keys()))
__EOF__
}

GEN_CACTUS=
GEN_SCATTER=
DEBUG=

while [ $# -gt 0 ]; do
    case $1 in
        -h|--help)
            echo "usage: $0 [<option>]"
            echo
            echo "options:"
            echo "   -h, --help    Print this mesasge and exit"
            echo "   -s, --scatter Produce scatter plots"
            echo "   -c, --cactus  Produce cactus plots"
            echo "   -d, --debug   Do not remove temporary file"
            echo
            exit
            ;;
        -s|--scatter)
            GEN_SCATTER=yes
            ;;
        -c|--cactus)
            GEN_CACTUS=yes
            ;;
        -d|--debug)
            DEBUG=yes
            ;;
        -*)
            echo "ERROR: invalid option '$1'"
            exit 1
            ;;
        *)
            break
    esac
    shift
done

tmpdir=$(mktemp -d)

[[ ! -z $DEBUG ]] || trap "rm -rf $tmpdir" EXIT

echo $tmpdir

mkdir -p figures

./make_solver_id_to_name_map.py -c $SOLVERS_CSV > $tmpdir/idToNameMap.csv

#for track in parallel cloud sq; do
for track in parallel cloud; do

    ./get_unsound_solvers_csv.sh \
        $RESULTS/results-${track}.csv \
        $tmpdir/idToNameMap.csv \
        > $tmpdir/unsound_solvers_${track}.csv
done

if [ ! -z $GEN_SCATTER ]; then
    # cvc5
    compare cvc5 cvc5-gg cloud
    compare cvc5 cvc5-gg parallel

    # Par4
    compare 2019-Par4 Par4 cloud
    compare 2019-Par4 Par4 parallel

    # STP
    compare STP STP-CMS-Cloud cloud
    compare STP STP-parallel parallel

    # Vampire
    compare Vampire Vampire-Parallel cloud
    compare Vampire Vampire-Parallel parallel

    # OpenSMT-portfolio
    compare OpenSMT 'SMTS portfolio' cloud

    # OpenSMT-cubeandconquer
    compare OpenSMT 'SMTS cube-and-conquer' cloud

    # OpenSMT-portfolio vs OpenSMT-cubeandconquer
    compare 'SMTS portfolio' 'SMTS cube-and-conquer' cloud
fi

if [ ! -z $GEN_CACTUS ]; then
#    for track in sq cloud parallel; do
    for track in cloud parallel; do
        if [ $track == "sq" ]; then
            track_long=single_query
        else
            track_long=$track
        fi

        for division in $(getDivisionNames $track); do
            csvcut -c 'solver id' ../scoring/results-$track.csv \
                    |sort |uniq |while read -r solver_id; do
                createCactusList "$track" "$solver_id" "$division"
            done \
                | $CACTUSPLOTTER \
                -d $division \
                -D $DIVISION_FILE \
                -t $track_long \
                -o figures/"$track"_"$division".svg \
                -c $SOLVERS_CSV \
                -u $tmpdir/unsound_solvers_$track.csv \
                -y 2021 \
                    > figures/"$track"_"$division".gp \
                && gnuplot figures/"$track"_"$division".gp
        done
    done
fi

