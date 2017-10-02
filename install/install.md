# Cluster Setup

This document will serve as a manual for cluster configuration.


## Overview

I used a total of six ec2 instances for this project.
Three nodes were used for kafka and zookeeper.
One node was used as a python producer.
One node was used for the PostgreSQL database.
One node was used to serve the flask web ui.


### Installation Instructions

The kafka cluster is built using pegasus (https://github.com/InsightDataScience/pegasus.git). I used a single master and two workers for cluster configuration (m4.large for each node). After the cluster is up, install the following packages via pegasus: ssh, zookeeper, kafka, and kafka-manager. Then I created a topic 'prod-test-topic' that has 6 partitions and a replication factor of 3.

The PostgreSQL node may then be started.
I followed the instructions here (https://github.com/snowplow/snowplow/wiki/Setting-up-PostgreSQL) and created a username, password, and database.
I created a table using the schema found in /test/test_db_classes.py and called the table 'prod_test_table'

The producer cluster may also be spun up via pegasus.
The node(s) need the kafka-python package, so go ahead and install that with pip.
Then this repo should be cloned into the node.

**Configuration Files**
There is a config directory at the top of the repo.
In it there are two template files: "db.config.template" and "kf.config.template".
Copy these files to db.config and kf.config, respectively.
The db.config file requires the credential information from the PostgreSQL node.
The kf.config file requires the host information from the kafka cluster.

Finally, the web-ui node may be started.
I used three tools for setting up the website: flask, tornado, and supervisor.
Flask is used for the html/css/javascript, tornado for server management, and supervisor for deployment. You'll want to install flask, tornado, and supervisor on this node.
You can either clone this repo to the web node at this point, or copy the contents of the webapp folder over. In the webapp folder, move the supervisor.conf to /etc/supervisor/supervisor.conf. Then run $supervisord from the command line.