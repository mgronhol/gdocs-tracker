#!/usr/bin/env python

import gdata.docs.service
import getpass, hashlib, time

def compute_hash( entry ):
	return hashlib.sha1( entry.title.text + entry.lastModifiedBy.name.text + entry.updated.text ).hexdigest()

def parse_time( ts ):
	(stamp, misc) = ts.split('.', 1)
	t = time.strptime( stamp, '%Y-%m-%dT%H:%M:%S' )
	return time.strftime( "[%Y-%m-%d %H:%M:%S]", t )

client = gdata.docs.service.DocsService()

user = raw_input( "Username: " )
pw = getpass.getpass()

client.ClientLogin( user, pw)

#db = {}

hashes = []

documents_feed = client.GetDocumentListFeed()
print ""
print "Current documents:"
for entry in documents_feed.entry:
	#print dir( document_entry )
	#print  entry.title.text, entry.lastModifiedBy.name.text, entry.updated.text
	hashes.append( compute_hash( entry ) )
	print parse_time( entry.updated.text ), entry.title.text, entry.lastModifiedBy.name.text, "(" + entry.lastModifiedBy.email.text + ")"

print ""
print ""
print "Modifications:"

try:
	while True:
		feed = client.GetDocumentListFeed()
		for entry in feed.entry:
			h = compute_hash( entry )
			if h not in hashes:
				#print entry.title.text, entry.lastModifiedBy.name.text, entry.updated.text
				print parse_time( entry.updated.text ), entry.title.text, entry.lastModifiedBy.name.text, "(" + entry.lastModifiedBy.email.text + ")"
				hashes.append( h )
		time.sleep( 30 )
except KeyboardInterrupt:
	pass



