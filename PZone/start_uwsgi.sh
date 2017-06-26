#!/bin/sh
echo "uWSGI Starting"
uwsgi --ini /mydata/www/PZone/pzone_uwsgi.ini
echo "uWSGI service is Started."
