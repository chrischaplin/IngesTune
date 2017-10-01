# Adapted from original kafka-prducer-performance script
# Adapted from jython benchmark script


import traceback
import time
import sys
import configparser
import psycopg2
sys.path.append("../srcPostgres")
sys.path.append("../srcMeasure")

from db_classes import pyToPostgres
from stats_classes import *


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
		

            kcs = {}
            try:
                with open("../../configs/kf.config") as myfile:
                    for line in myfile:
                        name, var = line.partition("=")[::2]
                        kcs[name.strip()] = str(var).strip('\n').strip(' ')
            except:
                print "Missing or invalid kf.config file -- look at kf.config.template for example usage"

            props['bootstrap_servers'] = kcs['bootstrap_servers']

                
            
            topic_name = 'test-topic-1'
            num_records = 100000

            producer = KafkaProducer(**props) 
            record = bytes(bytearray(record_size))
            stats = Stats(num_records, 1000)

            for i in xrange(num_records):
                send_start_ms = get_time_millis()
                future = producer.send(topic=topic_name, value=record)
                future.add_callback(stats.next_completion(
                        send_start_ms, record_size, stats))

            producer.close()

            
            rec = props
            rec['record_size'] = record_size            
            rec['max_in'] = rec.pop('max_in_flight_requests_per_connection')

            # Convert to int
            if rec['acks']=='all': rec['acks']=0
            
            del rec['bootstrap_servers']
            
            stats.print_total(rec)

            
        except Exception as e:

            print("Improper Usage, must include configuration")
            exc_info = sys.exc_info()
            traceback.print_exception(*exc_info)
            sys.exit(1)
            




if __name__ == '__main__':

    program_time = time.time()

    ProducerPerformance.run()
    
    print("--- %s seconds ---" % (time.time() - program_time))
    
