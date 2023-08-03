#!/bin/bash

mkdir out

while read -r ligne; do

	ligne_strip=$( echo $ligne | tr -d '\n' | tr -d '\r' )

	batiment=$(echo $ligne_strip | cut -f 1 -d ',' )
	salle=$(echo $ligne_strip | cut -f 2 -d ',' )
	url=$(echo $ligne_strip | cut -f 3 -d ',' )

	DTSTART=""
	DTEND=""
	SUMMARY=""

	file=$RANDOM.csv

	echo $batiment,$salle,$file >> out/salles.csv

	curl $url -f | while read -r ligne2; do
		code=$(echo $ligne2 | cut -f 1 -d ':' )
		value=$(echo $ligne2 | cut -f 2- -d ':' | tr -d '\n' | tr -d '\r' )

		if [[ $code == DTSTART ]] ; then
			DTSTART=$value
		elif [[ $code == DTEND ]] ; then
			DTEND=$value
		elif [[ $code == SUMMARY ]] ; then
			SUMMARY=$value
		elif [[ $code == END ]] && [[ $value == VEVENT ]]; then
			echo "$DTSTART,$DTEND,$SUMMARY" >> out/$file
		fi

	done

done < "$1"
