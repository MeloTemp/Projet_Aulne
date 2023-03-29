#!/bin/bash

I=0
TEMP_FILE=NOT_YET

for f in *.gz; do
	if ((I%2)); then
		echo "$TEMP_FILE $f"
		mkdir ../quality/$TEMP_FILE-quality
		fastqc $TEMP_FILE $f -o ../quality/$TEMP_FILE-quality
	else
		TEMP_FILE=$f
	fi
	I=$I+1
done

