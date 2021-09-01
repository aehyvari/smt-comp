### System for producing some analysis for cloud and parallel tracks

This directory contains scripts for producing analysis and publishing
them in the web page.  Web page production requires the installation of
the package [PyYaml](https://pyyaml.org/):

```
$ pip3 install pyyaml
```

*Note:* Before running the analysis, construct the final results files
by running the script `../scoring/clean_result_csvs.sh`.

To produce the analysis, type

```
$ ./plot.sh -s -c
```

and to publish the results, type

```
$ ./gen_mds.sh
```

The web page is produced from the markdown file `content/description.md`
using the script `./gen_mds.sh` that reads the results from `figures`
produced by the plot command above.
