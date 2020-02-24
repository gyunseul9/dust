#!/bin/bash

TIME=`date +"%Y-%m-%d_%H:%M:%S"`

if [ $# -lt 1 ]; then
	echo -e " "
	echo -e " usage: ./run.sh <value>"
	echo -e " e.g: ./run.sh ubuntu"
	exit 1;
else

	if [ ${1} = "local" ]; then
		DIR="/home/ubuntu/dust/"
	elif [ ${1} = "ubuntu" ]; then
		DIR="/home/ubuntu/dust/"
	else
		exit 1;
	fi

	source ${DIR}bin/activate

	for i in {1..17}
	do
		OUTPUT=$(python3 ${DIR}dust.py $i $1)
		echo -e "\n"$OUTPUT"\n"
		sleep 2
	done

fi
