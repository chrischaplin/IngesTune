# Reactive Streaming Pipeline

The purpose of this project is to design and implement a *reactive* streaming system as part of an end-to-end pipeline that involves streaming data ingestion, processing, and storage. By *reactive*, I mean a streaming pipeline that scales automatically with the incoming stream (self-tuning, self-stabilize, and self-heal). This is useful for any project that deals with a streaming data source. Specific use cases include handling dynamic stream rates (data **velocity** is non constant), complicated event processing (data **computation** is challenging), data skew (poor **distribution** of data between processing units), and tuning from scratch (user has no idea how many instances to spin up).

## Target Infrastructure

The infrastucture is completely centered on the streaming pipeline.


![alt](https://github.com/chrischaplin/reactiveStream/blob/master/figs/DE_Project_Pipeline.jpg)



## Reactive Abstraction

This project *still* ultimately intends to use the Dhalion[1] abstraction for self-regulation.

![alt](https://github.com/chrischaplin/reactiveStream/blob/master/figs/dhalion_abstract.png)



## Minimum Viable Product

The minimum viable product (MVP) will be focused on building a simple wrapper around Kafka.
The wrapper will manange a simple producer/topic/consumer paradigm.

![alt](https://github.com/chrischaplin/reactiveStream/blob/master/figs/MVP.jpg)