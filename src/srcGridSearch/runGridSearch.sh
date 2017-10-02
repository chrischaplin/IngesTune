#
#
# Script to (1) Run grid-searh
#           (2) Store results in PostgreSQL
#
#
#


# Grab the number of files
numfiles=`wc -l < ../srcConfigGen/prodConf/config.list`
echo ${numfiles}

# Set the numer of records for the test
num_records=50000

# Set the topic name
topic_name='prod-test-topic'

# Set the table name
table_name='prod_test_table'


# Loop over files
i=1
while [ $i -le $numfiles ]; do
    filename=`sed "${i}q;d" ../srcConfigGen/prodConf/config.list`

    # Loop over record size (10^j)
    for j in `seq 1 4`; do
	recsize=$((10**j))
	echo "python runProducer.py ../srcConfigGen/prodConf/${filename} ${recsize} ${num_records} ${topic_name} ${table_name}"
	python runProducer.py ../srcConfigGen/prodConf/${filename} ${recsize} ${num_records} ${topic_name} ${table_name}
    done

    i=$(($i+1))
done

