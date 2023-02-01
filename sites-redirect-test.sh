#! /usr/bin/env

URLS='sites.wikimedia.se
www.offentligkonst.se
offentligkonst.se
api.offentligkonst.se
odok.wikimedia.se
umepedia.se
www.umepedia.se
umea.wikimedia.se
map.wikilovesearth.se
'

for url in $URLS;
do
    curl -Ls -o /dev/null -w "%{url_effective}" http://$url | egrep --color=always "|http:" | tr -d '\n'
    echo " <= http://$url"
    curl -Ls -o /dev/null -w "%{url_effective}" https://$url
    echo " <= https://$url"
done
