# Adapted from original kafka-prducer-performance script
# Adapted from jython benchmark script


import traceback
import time
import sys
import configparser
import psycopg2

from kafka import KafkaProducer



class ProducerPerformance(object):

    @staticmethod
    def run():

        parser = configparser.SafeConfigParser()

        try:

            # Grab the configuration(s)
            parser.read(sys.argv[1])

	    # Grab the record size
	    record_size = int(sys.argv[2])

            props = {}
            for (each_key, each_val) in parser.items('producer_config'):
                try:
                    each_val = int(each_val)
                except ValueError:
                    pass
		if (each_val=='None'): each_val=None
                props[each_key] = each_val
		

            # Hard-coding these for now
            props['bootstrap_servers'] = 'localhost:9092'
            topic_name = 'prod-test-topic'

            # Reduced number of records for faster grid-search
            num_records = 50000

            producer = KafkaProducer(**props) 
            record = bytes(bytearray(record_size))
            stats = Stats(num_records, num_records)

            for i in xrange(num_records):
                send_start_ms = get_time_millis()
                future = producer.send(topic=topic_name, value=record, partition=0)
                future.add_callback(stats.next_completion(
                        send_start_ms, record_size, stats))

            producer.close()

            compr_str = props['compression_type']
	    if (compr_str == None): compr_str = 'None'
	

            stats.print_total(record_size,props['batch_size'],props['linger_ms'],props['max_in_flight_requests_per_connection'],compr_str,props['acks'])

            
        except Exception as e:

            print("Improper Usage, must include configuration")
            exc_info = sys.exc_info()
            traceback.print_exception(*exc_info)
            sys.exit(1)
            



class Stats(object):

    def __init__(self, num_records, reporting_interval):
        self.start = get_time_millis()
        self.window_start = get_time_millis()
        self.index = 0
        self.iteration = 0
        self.sampling = int(num_records / min(num_records, 500000))
        self.latencies = [0] * (int(num_records / self.sampling) + 1)
        self.max_latency = 0
        self.total_latency = 0
        self.window_count = 0
        self.window_max_latency = 0
        self.window_total_latency = 0
        self.window_bytes = 0
        self.count = 0
        self.bytes = 0
        self.reporting_interval = reporting_interval

    def record(self, iter, latency, bytes, time):
        self.count += 1
        self.bytes += bytes
        self.total_latency += latency
        self.max_latency = max(self.max_latency, latency)
        self.window_count += 1
        self.window_bytes += bytes
        self.window_total_latency += latency
        self.window_max_latency = max(self.window_max_latency, latency)
        if iter % self.sampling == 0:
            self.latencies[self.index] = latency
            self.index += 1

        if time - self.window_start >= self.reporting_interval:
            self.print_window()
            self.new_window()

    def next_completion(self, start, bytes, stats):
        cb = PerfCallback(self.iteration, start, bytes, stats).on_completion
        self.iteration += 1
        return cb

    def print_window(self):
        elapsed = get_time_millis() - self.window_start
        recs_per_sec = 1000.0 * self.window_count / float(elapsed)
        mb_per_sec = 1000.0 * self.window_bytes / float(elapsed) / (1024.0 * 1024.0)

        print '{0} records sent, {1} records/sec ({2} MB/sec), {3} ms avg ' \
              'latency, {4} max latency.'.format(
                self.window_count,
                recs_per_sec,
                mb_per_sec,
                self.window_total_latency / float(self.window_count),
                float(self.window_max_latency)
        )

    def new_window(self):
        self.window_start = get_time_millis()
        self.window_count = 0
        self.window_max_latency = 0
        self.window_total_latency = 0
        self.window_bytes = 0

    def print_total(self,record_size,batch_size,linger_ms,max_in_flight_requests_per_connection,compression_type,acks):
        elapsed = get_time_millis() - self.start
        recs_per_sec = 1000.0 * self.count / float(elapsed)
        mb_per_sec = 1000.0 * self.bytes / float(elapsed) / (1024.0 * 1024.0)

	print 'Num Indices:{0}'.format(self.index) 

        percs = self.percentiles(
                self.latencies, self.index, [0.5, 0.95, 0.99, 0.999])

        print '{0} records sent, {1} records/sec ({2} MB/sec), {3} ms avg ' \
              'latency, {4} ms max latency, {5} ms 50th, {6} ms 95th, {7} ' \
              'ms 99th, {8} ms 99.9th.'.format(
                self.count,
                recs_per_sec,
                mb_per_sec,
                self.total_latency / float(self.count),
                float(self.max_latency),
                percs[0],
                percs[1],
                percs[2],
                percs[3]
	)


	db = {}
        try:
	    with open("db.config") as myfile:
    		for line in myfile:
        		name, var = line.partition("=")[::2]
        		db[name.strip()] = str(var).strip('\n').strip(' ')
        except:
            print "Missing or invalid db.config file -- look at db.config.template for example usage"

	cs = "dbname={0} user={1} host={2} password={3}".format(db['dbname'],db['user'],db['host'],db['password'])

	

	try:
	    conn = psycopg2.connect(cs)
	except:
    	    print "I am unable to connect to the database"


	cur = conn.cursor()

	cur.execute("INSERT INTO test_final_table (throughput,latency,record_size,batch_size,linger_ms,max_in,comp,acks) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);",(mb_per_sec,percs[3],record_size,batch_size,linger_ms,max_in_flight_requests_per_connection,compression_type,acks))

	conn.commit()

	cur.close()
	conn.close()

        

    @staticmethod
    def percentiles(latencies, count, percentiles):
        size = min(count, len(latencies))
        latencies = latencies[:size]
        latencies.sort()
        values = [1] * len(percentiles)
        for i in xrange(len(percentiles)):
            index = int(percentiles[i] * size)
            values[i] = latencies[index]

        return values


class PerfCallback(object):

    def __init__(self, iter, start, bytes, stats):
        self.start = start
        self.stats = stats
        self.iteration = iter
        self.bytes = bytes

    def on_completion(self, metadata):
        now = get_time_millis()
        latency = int(now - self.start)
        self.stats.record(self.iteration, latency, self.bytes, now)


def get_time_millis():
    return time.time() * 1000


if __name__ == '__main__':

    program_time = time.time()

    ProducerPerformance.run()
    
    print("--- %s seconds ---" % (time.time() - program_time))
    
