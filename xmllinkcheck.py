#!/usr/bin/python
'''
Checks for link availability within XML documents and saves the url 
and the timestamp of the checking into the database.

    --	Jaakko Lappalainen 2014. jkk.lapp@gmail.com  --

This program is free software: you can redistribute it and/or modify 
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

'''
import urllib2,sys
from urllib2 import HTTPError
import MySQLdb
import time,re
import xml.etree.ElementTree as ET
import ConfigParser

# Command line argument checking
if len(sys.argv) != 2:
	print 'usage: ./xmllinkcheck <xml-file>'
	sys.exit(-1)

# Configuration
config = ConfigParser.RawConfigParser()
config.read('xmllinkcheck.cfg')
port = config.getint('DB', 'port')
host = config.get('DB', 'host')
user = config.get('DB', 'user')
passwd = config.get('DB', 'pass')
db = config.get('DB', 'db')

# Read file and find URLs
xml = open(sys.argv[1],'r').read()
urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', xml)
xml.close()

# Check each URL
for u in urls:
	try:
		#print u
		response = urllib2.urlopen(u)
	except HTTPError:
		conn = MySQLdb.connect(host=host,port=port, user=user, passwd=passwd, db=db)
		c = conn.cursor()
		try:
	    		c.execute("""INSERT INTO entries(dataset_id,url,timestamp) VALUES (%s,%s,%s)""",(sys.argv[1],u,str(int(time.time()))))
	   		conn.commit()
			conn.close()
		except Exception as e:
			print e
	   		conn.rollback()
			conn.close()


