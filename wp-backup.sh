#! /usr/bin/env bash

host=$(sudo php -r "include('$1'); echo DB_HOST;")
db=$(sudo php -r "include('$1'); echo DB_NAME;")
user=$(sudo php -r "include('$1'); echo DB_USER;")
password=$(sudo php -r "include('$1'); echo DB_PASSWORD;")

mysqldump --add-drop-table -h $host -u $user --password=$password $db | bzip2 -c | pv -p --timer --rate --bytes > backup-$(date --iso-8601).sql.bz2
