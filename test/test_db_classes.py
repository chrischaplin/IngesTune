import sys
sys.path.append("../src/srcPostgres")
from db_classes import pyToPostgres

import time


def run():

    table_schema = '(id serial PRIMARY KEY,throughput float8,latency float8,record_size int8,batch_size int8,linger_ms int8, max_in int8, acks int8)'

    db={}
    dbWrapper = pyToPostgres(db)
    dbWrapper = dbWrapper.fromConfig("../configs/db.config")


    dbWrapper.openConnection()

    dbWrapper.createTable('test_db_classes_table',table_schema)
    
    rec = { 'throughput':100.0, \
            'latency':10.0, \
            'record_size':10 , \
            'batch_size':80000, \
            'linger_ms':10, \
            'max_in':5, \
            'acks':-1}


    dbWrapper.insertIntoTable(rec,'test_db_classes_table')
    
    dbWrapper.printTable('test_db_classes_table')

    dbWrapper.deleteTable('test_db_classes_table')
    
    dbWrapper.closeConnection()




if __name__ == '__main__':

    program_time = time.time()

    run()
    
    print("--- %s seconds ---" % (time.time() - program_time))
