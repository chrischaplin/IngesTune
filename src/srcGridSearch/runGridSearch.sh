#
#
# Script to run grid-search and store results in PostgreSQL
#
#



# Grab the number of files
numfiles=`wc -l < ../srcConfGen/prodConf/config.list`


# Loop over files
i=1
while [ $i -le $numfiles ]; do
    filename=`sed "${i}q;d" ../confGen/config.list`

    # Loop over record size (10^j)
    for j in `seq 1 4`; do
	recsize=$((10**j))
	echo "python testSystem.py ../srcConfGen/prodConf/${filename} ${recsize}"
	python testSystem.py ../srcConfGen/prodConf/${filename} ${recsize}
    done

    i=$(($i+1))
done

