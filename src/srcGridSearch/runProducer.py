#
#
# This is an executable that measures throughput and latency
# for an input set of producer configurations and message size
#
# Results are stored in a postgreSQL database (name is hardcoded in srcMeasure/stats_classes.py)
#
#


# Python code translated from java kafka-prducer-performance script
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

            # Grab the number of records
            num_records = int(sys.argv[3])

            # Grab the topic
            topic_name = str(sys.argv[4])

            # Grab the table name
            table_name = str(sys.argv[5])

            
            
            # Get the grid-search parameters
            props = {}
            for (each_key, each_val) in parser.items('producer_config'):
                try:
                    each_val = int(each_val)
                except ValueError:
                    pass
		if (each_val=='None'): each_val=None
                props[each_key] = each_val

                
            # Get the bootstrap-servers
            kcs = {}
            try:
                with open("../../configs/kf.config") as myfile:
                    for line in myfile:
                        name, var = line.partition("=")[::2]
                        kcs[name.strip()] = str(var).strip('\n').strip(' ')
            except:
                print "Missing or invalid kf.config file -- look at kf.config.template for example usage"

            props['bootstrap_servers'] = kcs['bootstrap_servers']


            # Build Producer, test record of size(record_size), and stats class
            producer = KafkaProducer(**props) 
            record = bytes(bytearray(record_size))
            stats = Stats(num_records)

            
            # Run tests
            for i in xrange(num_records):
                send_start_ms = get_time_millis()
                future = producer.send(topic=topic_name, value=record)
                future.add_callback(stats.next_completion(
                        send_start_ms, record_size, stats))

            producer.close()

            
            # Compue the final stats
            (throughput,latency) = stats.get_total_stats()


            # Use the props dict to build out the remaining db record
            rec = props            
            rec['record_size'] = record_size            
            rec['max_in'] = rec.pop('max_in_flight_requests_per_connection')

            # Convert to int
            if rec['acks']=='all': rec['acks']=0

            # Remove the server information
            del rec['bootstrap_servers']
            
            rec['latency'] = latency
            rec['throughput'] = throughput

            
            # Open database
            db={}
	    dbWrapper = pyToPostgres(db)
	    dbWrapper = dbWrapper.fromConfig('../../configs/db.config')
	    dbWrapper.openConnection()

            # Write record and close database
            dbWrapper.insertIntoTable(rec,table_name)
	    dbWrapper.closeConnection()        
            

            
        except Exception as e:

            print("Improper Usage, must include configuration")
            exc_info = sys.exc_info()
            traceback.print_exception(*exc_info)
            sys.exit(1)
            




if __name__ == '__main__':


    ProducerPerformance.run()
