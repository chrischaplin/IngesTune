# IngesTune
## Performance tuning for Apache Kafka

The purpose of this project was to build a tuning framework around Apache Kafka.
Kafka is a distributed ingestion tool used in a wide variety of big data platforms.

So what is the challenge with ingestion?
Distributed ingestion technologies used in production are extremely powerful and extremely configurable.
Kafka in particular has O(100) configuration parameters.
Static configuration parameters include producer, consumer, and broker configurations.
Many topic configurations can be changed dynamically.
The default set of configurations are fine for many use cases (i.e. they will work for many applications out of the box), but a lot of potential performance is being left behind.

This project implements a grid search framework to find improved configuration parameters.
The grid search code is implemented in python and can generate a large number of configuration sets for each type of configuration (all user specified).
For this project, producer configurations were investigated (batch_size, linger_ms, max_in_flight_requests_per_connection, and acks).
The code measures throughput and latency as proxies for typical service level objectives.
The output is the set of configuration values that produced the best performance.


## Project Pipeline

![alt](https://github.com/chrischaplin/IngesTune/blob/master/figs/pipeline.png)

The pipeline consists of a python producer passing data into the testing framework built around Kafka.
While the producer is running, throughput and latency are being computed and sent to a PostgreSQL database for querying at completion.
Another python node is used to display the final results on a website.
Two plots are rendered comparing the performance of the tuned producer to the default producer.


## Results

I built several test producers using the Kafka python API.
Each producer repeatedly sent a constant length (10,100,1000,10000) byte array message to Kafka.
The results are presented below.

[Ingestune Results](http://www.ingestune.com)

![alt](https://github.com/chrischaplin/IngesTune/blob/master/figs/throughput.png)
![alt](https://github.com/chrischaplin/IngesTune/blob/master/figs/latency.png)

The tuner was able to double throughput, compared to the default producer configuation, for all of the tested message sizes.
As for latency, it was difficult to beat the default settings except for larger message sizes.
Removing the acknowledgement requirement cut the latency by at least 2x over all message sizes.


## Usage

Look at install/install.md for cluster setup.

Run test/test_db_classes.py and test/test_runProducer.py to check the connection and functionality to the PostgreSQL database and the Kafka cluster respectively.
If these two tests pass, the rest of the code will work.

There are three shell scripts that run the grid search and generate the results:
1.  src/srcConfigGen/prodConf/makeConfig.sh -- generates the grid search configs
2.  src/srcGridSearch/runGridSearch.sh -- runs over the grid search to produce throughput and latency for each config
3.  src/srcPostgres/generateResults.sh -- writes out the results
