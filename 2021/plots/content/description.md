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
[here](parallel-and-cloud-tracks-participation.html) for documentation
purposes.



### Solver comparisons in cloud track

The cactus plots below show results on the solvers submitted to the
cloud track as well as solvers that ran on single-query
track that I ran on starexec.  The cloud track solvers are plotted with
a thicker line.  An asterisk after a solver name indicates that it was
unsound in the division in the cloud track.

{% assign cactus_cloud = page.figures |where: "type", "cactus" |where: "track", "cloud" %}
{% for pic in cactus_cloud %}
#### Track cloud, Division {{ pic.division }}
  <img src="par-cloud-analysis/{{ pic.name }}.svg"/>
  {% if pic.unsound %}
  - Unsound solvers on this track and division:
    {% for solver in pic.unsound %}
    - {{ solver.name }}
    {% endfor %}
  {% endif %}
{% endfor %}

{% assign cactus_parallel = page.figures |where: "type", "cactus" |where: "track", "parallel" %}
{% for pic in cactus_parallel %}
#### Track parallel, Division {{ pic.division }}
  <img src="par-cloud-analysis/{{ pic.name }}.svg"/>
  {% if pic.unsound %}
  - Unsound solvers on this track and division:
    {% for solver in pic.unsound %}
    - {{ solver.name }}
    {% endfor %}
  {% endif %}
{% endfor %}


#### Version comparisons in the cloud track

A version of these solvers were submitted in both cloud and single-query
tracks, allowing a comparison between the two versions.  In case of
SMTS, two versions were submitted to the cloud track.

{% assign scatter_cloud = page.figures |where: "type", "scatter" |where: "track", "cloud" %}
{% for pic in scatter_cloud %}
  <img src="par-cloud-analysis/{{ pic.name }}.svg"/>
  - {{ pic.x-axis }} solved {{ pic.x-solved }} instances.
  - {{ pic.y-axis }} solved {{ pic.y-solved }} instances.
  - {{ pic.y-axis }} is in total {{ pic.total_speedup | round: 2}} times faster than
    {{ pic.x-axis }}
  - {{ pic.y-axis }} is on average {{ pic.average_speedup | round: 2}} times faster than
    {{ pic.x-axis }}
  {% if pic.unsound %}
  - Unsoundnesses:
    {% for unsoundness in pic.unsound %}
    - {{ unsoundness.solver }} is unsound on `{{ unsoundness.instance }}`
    {% endfor %}
  {% endif %}
{% endfor %}


#### Version comparisons in the parallel track

A version of these solvers were submitted in both parallel and single-query
tracks, allowing a comparison between the two versions.

{% assign scatter_parallel = page.figures |where: "type", "scatter" |where: "track", "parallel" %}
{% for pic in scatter_cloud %}
  <img src="par-cloud-analysis/{{ pic.name }}.svg"/>
  - {{ pic.x-axis }} solved {{ pic.x-solved }} instances.
  - {{ pic.y-axis }} solved {{ pic.y-solved }} instances.
  - {{ pic.y-axis }} is in total {{ pic.total_speedup | round: 2}} times faster than
    {{ pic.x-axis }}
  - {{ pic.y-axis }} is on average {{ pic.average_speedup | round: 2 }} times faster than
    {{ pic.x-axis }}
  {% if pic.unsound %}
  - Unsoundnesses:
    {% for unsoundness in pic.unsound %}
    - {{ unsoundness.solver }} is unsound on `{{ unsoundness.instance }}`
    {% endfor %}
  {% endif %}
{% endfor %}

