#!/usr/bin/python

import psycopg2
import couchdb
from datetime import datetime, timedelta
import os

intervalAlert=7
intervalBlock=7

def getcouch(layer, server):
	SERVER_LIST={
	'2':'77.95.132.135',
	'9':'77.95.132.134',
	'10':'192.168.201.101', 
	'12':'192.168.202.101',
	'13':'192.168.202.102',
	'14':'192.168.202.103',
	'15':'localhost'
	}
	if server in (10, 12, 13, 14):
		cdbname = os.popen("./get_cdb_name.sh \"{0}\" \"{1}\"".format(layer, SERVER_LIST[str(server)])).read().strip("\n")
	return cdbname

def get_device_info(couchname):
	server = couchdb.Server('http://admin:admin@localhost:5984')
	db=server[couchname]
	res = db.iterview("_all_docs", 1, startkey='device_info', endkey='device_info', include_docs=True)
	for row in res:
        return row.id

janitor_connect = psycopg2.connect("dbname='janitordb' user='janitordb' host='localhost' password='janitordb'")
cur = janitor_connect.cursor()
cur.execute("select name, layer, tostoptime, database_id from customer where franchiser_id is null and database_id not in (1,3)")
res=cur.fetchall()

layer = res[1]
#for layer in res:
name = layer[0]
sys_name = layer[1]
layerStopTime = datetime.strftime(layer[2], "%Y-%m-%dT%H:%M:%SZ")
layerStopAlertTime = datetime.strftime(layer[2] - timedelta(days=intervalAlert), "%Y-%m-%dT%H:%M:%SZ")
terminalLockTime = datetime.strftime(layer[2] + timedelta(days=intervalBlock), "%Y-%m-%dT%H:%M:%SZ")
print (name, sys_name, layerStopAlertTime, layerStopTime, terminalLockTime)
print (getcouch("baton38", 15))


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