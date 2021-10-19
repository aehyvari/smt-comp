---
layout: default
plot_path: /2021/plot_data
plot_summary: plot_summary.html
---

## Parallel and Cloud Tracks

In 2021 the SMT-COMP included two new tracks for parallel solvers.  The
goal of these tracks is to showcase how such solvers fare against the
sequential solvers.

In total there were six parallel or cloud solvers that competed in the
new tracks, whereas the main competiton had 20 participants in the
single-query track.

A detailed analysis shows that the parallel solvers are often superior
to the solvers competing in the single-query track.  However, this is
not universally true, and depends on the division.

In this text I try to give my personal interpretation of the situation
from Summer 2021.  For the pictures only, see <a href="{{ page.plot_summary }}">here</a>

### The Concept

The parallel solvers competed in two tracks: the *cloud* and the
*parallel* tracks.  In both tracks the idea is to measure how fast a
solver solves single, hard instances.  We chose in total slightly over
400 benchmarks from the single-query track logics as the benchmarks.

The parallel and cloud tracks were run on Amazon Web Services
infrastructure.  The standard competition was run in StarExec.

### <a name="overview"></a> Overview of the Results

The solvers that competed in the parallel and cloud tracks can be
clearly faster than any of the solvers competing in the single-query
track.  However, they can also be slower or indeed "less reliable",
i.e., unsound.

As an example, the parallel version of
[Vampire](participants/vampire-parallel.html) wins the other solvers
with a convenient margin in the [cloud track's Equality
division](results/equality-cloud.html).

<img src="{{ page.plot_path }}/cloud_Equality.svg"/>

It is hard to give a single picture on the performance of solvers that
competed in the 2021 SMT competition parallel and cloud tracks. The SMT
competition, even when considering only the solvers designed to run in
the AWS infrastructure, consists of 18 tracks.  These tracks are
practically independent competitions because in general solvers support,
or are specialised on solving, a subset of these tracks.

For instance, the SMT-COMP [rules](rules.pdf) define track-wide
recognitions.  The following table gives the biggest lead ranking of the
cloud track competitors.

{% assign cloudBiggestLead = site.results_2021 |where: "track", "track_cloud" |where: "recognition", "biggest_lead" | first %}
{% assign participants = site[cloudBiggestLead.participants] %}
{% assign divisions = site.results_2021 |group_by: "track" |where: "name", "track_cloud" |first %}

<table id = "cloud-biggest-lead" class="result sorted">
<thead>
<tr>
<th>Solver</th>
<th>Correct Score</th>
<th>Time Score</th>
<th>Division</th>
<th>Plot</th>
</tr>
</thead>
{% for score in cloudBiggestLead.parallel %}
<tr>
<td>
    {% assign participant = participants | where: "name", score.name |first %}
<a href="{{ participant.url }}">{{ score.name }}</a>
</td>
<td>{{ score.correctScore }}</td>
<td>{{ score.timeScore }}</td>
<td>
    {% assign div = divisions.items |where: "division", score.division |first %}
<a href="{{ div.url }}">{{ score.division }}</a>
</td>
<td>
    {% assign plot = site.plots_2021 |where: "track", "cloud" |where: "division", score.division |first %}
<a href="{{  plot.url }}">{{ plot.name }}</a>
</td>
</tr>
{% endfor %}
</table>

Clicking through the results we can see for instance that in the seven
winning scores only four of the cases the awarded solver actually wins
all the competitors.

<p>

The rules also provide a score for the <em>largest contribution</em>
score. This year the score seems to a slightly more consistent view,
while it unfortunately, due to lack of competition, could be defined
only for two divisions (the winners in the table tracks are both my
solvers).

{% assign cloudLargestContribution = site.results_2021 |where: "track", "track_cloud" |where: "recognition", "largest_contribution" | first %}
{% assign participants = site[cloudLargestContribution.participants] %}
{% assign divisions = site.results_2021 |group_by: "track" |where: "name", "track_cloud" |first %}

<table id = "cloud-largest-contribution" class="result sorted">
<thead>
<tr>
<th>Solver</th>
<th>Correct Score</th>
<th>Time Score</th>
<th>Division</th>
<th>Plot</th>
</tr>
</thead>
{% for score in cloudLargestContribution.parallel %}
<tr>
<td>
    {% assign participant = participants | where: "name", score.name |first %}
<a href="{{ participant.url }}">{{ score.name }}</a>
</td>
<td>{{ score.correctScore }}</td>
<td>{{ score.timeScore }}</td>
<td>
    {% assign div = divisions.items |where: "division", score.division |first %}
<a href="{{ div.url }}">{{ score.division }}</a>
</td>
<td>
    {% assign plot = site.plots_2021 |where: "track", "cloud" |where: "division", score.division |first %}
<a href="{{  plot.url }}">{{ plot.name }}</a>
</td>
</tr>
{% endfor %}
</table>


