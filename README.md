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

This project implements a grid search framework to find improved configuration parameters. The grid search code is implemented in python and can generate a large number of configuration sets for each type of configuration (all user specified).
I measure throughput and latency as proxies for typical service level objectives.
The output is the set of configuration values that produced the best performance.


## Project Pipeline

![alt](https://github.com/chrischaplin/IngesTune/blob/master/figs/pipeline.png)

The pipeline consists of a python producer passing data into the testing framework built around Kafka. While the producer is running, throughput and latency are being computed and the final values are sent to a PostgreSQL database for querying at completion.
Another python node is used to display a webpage.
On the webpage, two plots are rendered comparing the performance of the tuned producer to the default producer.


## Results

I built several test producers.
Each producer repeatedly sent a constant length (10,100,1000,10000) byte array to Kafka.

[Ingestune Results](http://www.ingestune.com)


The tuner was able to double throughput for all of the tested message sizes.
![alt](https://github.com/chrischaplin/IngesTune/blob/master/figs/throughput.png)

Similarly, the tuner was able to improve the latency by a factor of two for each message size.
![alt](https://github.com/chrischaplin/IngesTune/blob/master/figs/latency.png)


## Usage

There are three shell scripts that control the flow of code.
1.  src/srcConfigGen/prodConf/makeConfig.sh -- generates the grid search configs
2.  src/srcGridSearch/runGridSearch.sh -- runs over the grid search to produce throughput and latency for each config
3.  src/srcPostgres/generateResults.sh -- writes out the results