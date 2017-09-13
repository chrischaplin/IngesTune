# Cluster Setup

This document will serve as a manual for cluster configuration.


## Batch Processing Cluster
The pegasus pipeline tool (examples/spark/…) works like a charm for simple Hadoop+Spark applications.

Todo: Need to explore the issue of setting up a database

## Streaming Processing Cluster
There are pegasus installation/configuration scripts for zookeeper, storm, and kafka. The question is if these are truly reliable and are they actually allowing us to build out our cluster in the correct manner.

### Heron
Using the following this blog post: [link](http://streamanalytics.blogspot.com/2016/06/deploying-heron-on-cluster-of-machines.html)

I am using terminator to manage broacasting to terminal groups.
The pegasus braodcast ssh tool could also work, but it is slower and more bulky.

Personal Notes:
* hdfs fs appears to be outdated, use hdfs dfs
* hdfs dfs -mkdir -p (p is required if a parent directory also must be created) 