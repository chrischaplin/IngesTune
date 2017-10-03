import sys

from kafka import KafkaProducer


def testConnection():
                
    # Get the bootstrap-servers
    props = {}
    try:
        with open("../configs/kf.config") as myfile:
            for line in myfile:
                name, var = line.partition("=")[::2]
                props[name.strip()] = str(var).strip('\n').strip(' ')
    except:
        print "Missing or invalid kf.config file -- look at kf.config.template for example usage"
        return 0

        
    try:
                
        # Build Producer, test record of size(record_size), and stats class
        producer = KafkaProducer(**props) 
        record = bytes(bytearray(10))

            
        # Send a single message
        for i in xrange(1):
            future = producer.send(topic='test', value=record)
            producer.close()
            
        return 1
    except:
        print "Unable to connect to kafka server and send message"
        return 0



def runTests():

    flag = testConnection()
    print 'Test Open Kafka Connection: {0}'.format(flag)

            

if __name__ == '__main__':


    runTests()
