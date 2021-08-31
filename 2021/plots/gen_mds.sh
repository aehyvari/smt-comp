#!/bin/bash
WEBROOT=../../../smt-comp.github.io/

#./plot.sh -c -s

(
    echo "---"
    echo "figures:"
    ls figures/*.png \
        | while read -r file; do
            bname=$(basename "$file")
            echo "- par-cloud-analysis/$bname"
            cp "$file" $WEBROOT/2021/par-cloud-analysis/"$bname"
        done
    echo "---"
    cat << __EOF__

## Parallel and Cloud Tracks

This year we are organising new, experimental, cloud and parallel tracks
for SMT-COMP.  Similar tracks were organised in the SAT competition 2020
and the competition had a positive impact on the development of parallel
SAT solvers (see <https://satcompetition.github.io/2020/>).

### The Concept

The goal in both the cloud and the parallel tracks is to measure the
success of a solver in solving a single, hard instance.  This will be done by
giving solvers instances one at a time, similar to the SMT-COMP single-query
track.  The participating solvers will be scored based on the number of
instances that a solver solves within the per-instance wall-clock time limit
and the total run time, similar to the single-query track’s parallel score.

For these tracks we chose in total slightly over 400 benchmarks from the
single-query track logics.  All instances should come from the smt-lib
benchmark library.

The solver submission rules follow those of the rest of the tracks.  However,
on this track we do accept portfolio solvers, as defined in the rules, as
competitors.  We encourage submission of non-portfolio solvers and reserve the
right to give special mentions to non-portfolio solvers in reporting the
results.

While the standard competition will be run in StarExec, the parallel and cloud
tracks will be run on Amazon Web Services.  AWS has kindly agreed to sponsor
the participants in the testing phase.

The information for participation is stored
[here](parallel-and-cloud-tracks-participation.html) for documentation purposes.

### Analysis of the results
{% for pic in page.figures %}
  foobar
  <img src="{{pic}}"/>
{% endfor %}
__EOF__

) > $WEBROOT/2021/parallel-and-cloud-tracks.md

