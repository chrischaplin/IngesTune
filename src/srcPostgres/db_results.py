from db_classes import pyToPostgres

import time


def run():

    db={}
    dbWrapper = pyToPostgres(db)
    dbWrapper = dbWrapper.fromConfig("../../configs/db.config")


    dbWrapper.openConnection()

    fh1 = open('latency_sync.txt', 'w')
    fh2 = open('latency_best.txt', 'w')
    fh3 = open('throughput.txt', 'w')
    

    for x in range(1, 5):

        lat_synccs = '{0},{1},{2}'.format(pow(10,x),dbWrapper.queryForLatencySync('prod_test_table',pow(10,x)),dbWrapper.queryForLatencyDefault('prod_test_table',pow(10,x)))
        fh1.write(lat_synccs + '\n')

        lat_bestcs = '{0},{1},{2}'.format(pow(10,x),dbWrapper.queryForLatency('prod_test_table',pow(10,x)),dbWrapper.queryForLatencyDefault('prod_test_table',pow(10,x)))
        fh2.write(lat_bestcs + '\n')

        thrcs = '{0},{1},{2}'.format(pow(10,x),dbWrapper.queryForThroughputSync('prod_test_table',pow(10,x)),dbWrapper.queryForThroughputDefault('prod_test_table',pow(10,x)))
        fh3.write(thrcs + '\n')
        
 
    fh1.close() 
    fh2.close()
    fh3.close()
    
        
    dbWrapper.closeConnection()




if __name__ == '__main__':

    run()
