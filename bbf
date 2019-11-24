#!/bin/sh

if [ "$1" = "build" ]
then 
	python bloom.py "${@:2}"
elif [ "$1" = "query" ]
then
	python query.py "${@:2}"
else
	echo "action not found"
fi
