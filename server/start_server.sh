#!/bin/sh

#
# Sync database and run Django server
#

if [ ! -f "po.db" ]
then
    python manage.py syncdb
fi

python manage.py runserver 0.0.0.0:8000
