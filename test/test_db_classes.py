import sys
sys.path.append("../src/srcPostgres")
from db_classes import pyToPostgres

import time



def testConnection():

    db={}
    dbWrapper = pyToPostgres(db)
    dbWrapper = dbWrapper.fromConfig("../configs/db.config")

    flag = 0
    
    try:
        dbWrapper.openConnection()
        flag = 1
    except:
        flag = 0

    return (dbWrapper,flag)




def testCreateTable(dbWrapper):

    table_schema = '(id serial PRIMARY KEY,throughput float8,latency float8,record_size int8,batch_size int8,linger_ms int8, max_in int8, acks int8)'

    try:
        dbWrapper.createTable('test_db_classes_table',table_schema)
        return 1
    except:
        return 0

    


def testInsert(dbWrapper):

    rec = { 'throughput':100.0, \
            'latency':10.0, \
            'record_size':10 , \
            'batch_size':80000, \
            'linger_ms':10, \
            'max_in':5, \
            'acks':-1}

    try:
        dbWrapper.insertIntoTable(rec,'test_db_classes_table')
        return 1
    except:
        return 0

    

def testPrint(dbWrapper):

    try:
        dbWrapper.printTable('test_db_classes_table')
        return 1
    except:
        return 0


def testDelete(dbWrapper):

    try:
        dbWrapper.deleteTable('test_db_classes_table')
        return 1
    except:
        return 0

def testCloseConnect(dbWrapper):

    try:
        dbWrapper.closeConnection
        return 1
    except:
        return 0

    

    
    
def runTests():


    (dbWrapper,flag) = testConnection()
    print 'Test Open Connection: {0}'.format(flag)
    
    flag = testCreateTable(dbWrapper)
    print 'Test Table Create: {0}'.format(flag)
    
    flag = testInsert(dbWrapper)
    print 'Test Insertion: {0}'.format(flag)
    
    flag = testPrint(dbWrapper)
    print 'Test Print: {0}'.format(flag)
    
    flag = testDelete(dbWrapper)
    print 'Test Delete Table: {0}'.format(flag)
    
    flag = testCloseConnect(dbWrapper)
    print 'Test Close Connection: {0}'.format(flag)




if __name__ == '__main__':

    runTests()
