# Cluster Setup

This document will serve as a manual for cluster configuration.


## Overview

I used a total of six ec2 instances for this project.
Three nodes were used for kafka and zookeeper.
One node was used as a python producer.
One node was used for the PostgreSQL database.
One node was used to serve the flask web ui.


### Installation Instructions

The kafka cluster is built using pegasus (https://github.com/InsightDataScience/pegasus.git).
The configuration file(s) and start up script are in the kafka-cluster sub-directory.

Finish this later...
