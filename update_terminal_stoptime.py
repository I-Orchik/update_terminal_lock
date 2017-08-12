#!/usr/bin/python

import psycopg2
import couchdb
from datetime import datetime, timedelta
import os
#from sshtunnel import SSHTunnelForwarder
#import paramiko

intervalAlert=7
intervalBlock=7

def getcouch(layer, server):
	SERVER_LIST={
	'Juggernaut':'77.95.132.135'
	'Neo':''

	}


	cdbname = os.popen("ssh root@192.168.201.101 \"su - postgres -c './scripts/get_cdb.sh batman'\"").read().strip('\n')
	print(cdbname)

def select_server(server):


janitor_connect = psycopg2.connect("dbname='janitordb' user='janitordb' host='localhost' password='janitordb'")
cur = janitor_connect.cursor()
cur.execute("select c.name, c.layer, c.tostoptime, ds.name from customer c left join databaseserver ds on ds.id=c.database_id where c.franchiser_id is null and c.database_id not in (1,3)")
res=cur.fetchall()

layer = res[1]
#for layer in res:
name = layer[0]
sys_name = layer[1]
layerStopTime = datetime.strftime(layer[2], "%Y-%m-%dT%H:%M:%SZ")
layerStopAlertTime = datetime.strftime(layer[2] - timedelta(days=intervalAlert), "%Y-%m-%dT%H:%M:%SZ")
terminalLockTime = datetime.strftime(layer[2] + timedelta(days=intervalBlock), "%Y-%m-%dT%H:%M:%SZ")
print (name, sys_name, layerStopAlertTime, layerStopTime, terminalLockTime)
getcouch("batman")

	#with SSHTunnelForwarder((REMOTE_HOST),
	#	ssh_username='root',
	#	remote_bind_address=('localhost', PORT),
	#   local_bind_address=('localhost', PORT)):
	#	print("try connect to database...")
	#	dbconn = psycopg2.connect("dbname='dbbatman' user='dbbatman' host='localhost' port=5432 password='dbbatman'")
	#	dbcurs = dbconn.cursor()
	#	dbcurs.execute("select name from couchdb")
	#	cdbname=dbcurs.fetchall()[0]
	#	print(cdbname)
	#	PORT=5432
	#REMOTE_HOST="192.168.201.101"
	#REMOTE_SSH_PORT=22
	#print("try connect to remote server...")
	#t = paramiko.Transport((REMOTE_HOST, 22))
	#print("Transport opened.")
	#t.connect(username="root")
	#print("Connected") 
	#c = paramiko.Channel(t)
	#print("Channel opened.")
	#dbconn = psycopg2.connect("dbname='dbbatman' user='dbbatman' host='192.168.202.101' port=5432 password='dbbatman'")
	#curs = conn.cursor()
	#dbcurs = dbconn.cursor()
	#dbcurs.execute("select name from couchdb")
	#cdbname=dbcurs.fetchall()