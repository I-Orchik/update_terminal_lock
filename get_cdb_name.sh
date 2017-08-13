#!/usr/bin/env bash

LAYER=$1
DB_IP=$2
SQL="select name from couchdb where login='$1'"

ssh -M -S /tmp/ssh_psql.sock -fnNT -L 15432:$DB_IP:5432 root@$DB_IP 2> /dev/null

PGPASSWORD=db$LAYER psql -h127.0.0.1 -Aqt -p15432 -Udb$LAYER -c "$SQL" db$LAYER

ssh -S /tmp/ssh_psql.sock -O exit postgres@$DB_IP 2> /dev/null
