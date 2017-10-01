import psycopg2




# This is a wrapper around psycopg2 (python-postgreSQL) 
class pyToPostgres:    
    _db_conn = None    
    _db_curs = None


    def __init__(self,credentials):
        # Credentials is a dict of access paramaters
        # (dbname, user, host, password)
        self.credentials = credentials
        self.isOpen      = False


        

    @classmethod
    def fromConfig(instance,configFile):
        credentials = {}
        try:
            with open(configFile) as myfile:
    	        for line in myfile:
                    name, var = line.partition("=")[::2]
                    credentials[name.strip()] = str(var).strip('\n').strip(' ')
        except:
            print "Missing or invalid config file -- look at db.config.template for example usage"


        return instance(credentials)
            


    
    def openConnection(self):

        
        commandString = "dbname={0} user={1} host={2} password={3}".format(self.credentials['dbname'],self.credentials['user'],self.credentials['host'],self.credentials['password'])

	try:
	    self._db_conn = psycopg2.connect(commandString)
	    self._db_curs = self._db_conn.cursor()
	    self.isOpen = True
            
	except:
	    print "Unable to open database"
	    self.isOpen = False
        


            
    def closeConnection(self):

        assert self.isOpen
        
        self._db_conn.close()
        self._db_curs.close()
    
	self.isOpen = False



        
    def insertIntoTable(self,record,table_name):
        # Record should be a dict        
        assert self.isOpen        


        keys = ", ".join(record.keys())
        keys.strip("'")

        values = record.values()
        values = ','.join(str(v) for v in values)

        
        cs = "INSERT INTO {0} ({1}) VALUES ({2});".format(table_name, \
                                                          keys, \
                                                          values)

        self._db_curs.execute(cs)

        self._db_conn.commit()



        
    def createTable(self,table_name,schema):
        # schema is a string of column names and types

        # For reference, here is what a "schema" should look like:
        #(id serial PRIMARY KEY,throughput float8,latency float8, \
        #record_size int8,batch_size int8,linger_ms int8, max_in int8, \
        #comp varchar, acks int8)
        assert self.isOpen

        cs = "CREATE TABLE {0} {1};".format(table_name,schema)

        
        self._db_curs.execute(cs)

        self._db_conn.commit()
        


        
    def deleteTable(self,table_name):

        assert self.isOpen

        cs = "DROP TABLE {0}".format(table_name)

        self._db_curs.execute(cs)

        self._db_conn.commit()
        


        
        
    def queryForLatency(self,table_name,record_size):

        assert self.isOpen

        cs = "SELECT * from {0} where record_size = {1} ORDER By latency ASC;".format(table_name,record_size)
        
        self._db_curs.execute(cs)        

        self._db_conn.commit()

        rows = self._db_curs.fetchall()

        print rows[0]




    def queryForThroughput(self,table_name,record_size):

        assert self.isOpen

        cs = "SELECT * from {0} where record_size = {1} ORDER By throughput DESC;".format(table_name,record_size)
        
        self._db_curs.execute(cs)        

        self._db_conn.commit()

        rows = self._db_curs.fetchall()

        print rows[0]


            


    def printTable(self,table_name):

        assert self.isOpen

        cs = "SELECT * from {0};".format(table_name)
        
        self._db_curs.execute(cs)

        rows = self._db_curs.fetchall()

	print "\nShow me the rows:\n"
	for row in rows:
    	    print row

        
        self._db_conn.commit()
        


        
    def __del__(self):

        if self.isOpen:

            self._db_curs.close()
            self._db_conn.close()
