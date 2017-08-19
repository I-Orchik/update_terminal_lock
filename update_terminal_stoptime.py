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
	if server == 15:
		cdbname = 'startup_baton38'
	return cdbname


def get_device_info_doc(couch):
	docs = couch.iterview("_all_docs", 1, startkey='device_info', endkey='device_info{', include_docs=True)
	for row in docs:
		return row.id


def generate_update_doc(doc, layerStopTime, layerStopAlertTime, terminalLockTime):
	oldLayerStopTime = doc.get('layerStopTime')
	oldLayerStopAlertTime = doc.get('layerStopAlertTime')
	oldTerminalLockTime = doc.get('terminalLockTime')
	if (layerStopTime!=oldLayerStopTime) or (oldLayerStopAlertTime!=layerStopAlertTime) or (oldTerminalLockTime!=terminalLockTime):
		doc['layerStopTime'] = layerStopTime
		doc['layerStopAlertTime'] = layerStopAlertTime
		doc['terminalLockTime'] = terminalLockTime
		return doc
	return None


janitor_connect = psycopg2.connect("dbname='janitordb' user='janitordb' host='localhost' password='janitordb'")
cur = janitor_connect.cursor()
#cur.execute("select name, layer, tostoptime, database_id from customer where franchiser_id is null and database_id not in (1,3)")
cur.execute("select name, layer, tostoptime, database_id from customer where name='baton38'")

res=cur.fetchall()
layer = res[0]
#for layer in res:
if 1:
	name = layer[0]
	sys_name = layer[1]
	layerStopTime = datetime.strftime(layer[2], "%Y-%m-%dT%H:%M:%SZ")
	layerStopAlertTime = datetime.strftime(layer[2] - timedelta(days=intervalAlert), "%Y-%m-%dT%H:%M:%SZ")
	terminalLockTime = datetime.strftime(layer[2] + timedelta(days=intervalBlock), "%Y-%m-%dT%H:%M:%SZ")
	couchname = getcouch("baton38", 15)
	server = couchdb.Server('http://admin:admin@localhost:5984')
	db = server[couchname]
	device_info_id = get_device_info_doc(db)
	new_doc = generate_update_doc(db[device_info_id], layerStopTime, layerStopAlertTime, terminalLockTime)
	if new_doc is not None:
		db[device_info_id] = new_doc
		print "Doc {0} updated".format(device_info_id)
	else:
		print "Doc not updated"
	print "Check cdb"