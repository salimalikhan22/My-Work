#!/bin/bash


array=()

for A in $(ls -l /home/master/applications/| grep "^d" | awk '{print $NF}'); do 
	echo "Application: $A" 
	cd /home/master/applications/$A/public_html/
	if wp core is-installed; then 
		wp config set DISABLE_WP_CRON true --raw
		url=$(wp option get siteurl)
		line=$(cat /home/master/applications/$A/conf/server.nginx)
		domain=$(echo "$line" | grep -oE '[a-zA-Z0-9-]+\.cloudwaysapps\.com' | awk '{print $1}')
		data_json="{\"FQDN\": \"$domain\", \"URL\": \"$url\",\"APPNAME\": \"$A\" }"
		array+=("$data_json")
	fi; 
	json_data="[$(IFS=,; echo "${array[*]}")]"
	
#	echo "$json_data"	
	echo "$json_data" > /home/master/applications/$1/tmp/data.json
done

echo "$(cat /home/master/applications/$1/tmp/data.json)"
