from db_classes import pyToPostgres

import time


def run():

    db={}
    dbWrapper = pyToPostgres(db)
    dbWrapper = dbWrapper.fromConfig("../../configs/db.config")


    dbWrapper.openConnection()


    fh1 = open('latency.txt', 'w')
    fh2 = open('throughput.txt', 'w')    

    for x in range(1, 5):

        latcs = '{0},{1},{2}'.format(pow(10,x),dbWrapper.queryForLatency('prod_test_table',pow(10,x)),dbWrapper.queryForLatencyDefault('prod_test_table',pow(10,x)))
        fh1.write(latcs + '\n')

        thrcs = '{0},{1},{2}'.format(pow(10,x),dbWrapper.queryForThroughput('prod_test_table',pow(10,x)),dbWrapper.queryForThroughputDefault('prod_test_table',pow(10,x)))
        fh2.write(thrcs + '\n')
        
    fh1.close() 
    fh2.close()
    
        
    dbWrapper.closeConnection()




if __name__ == '__main__':

    run()
