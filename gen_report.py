'''
Checks for two unavailability entries in the DB for in less 
than a month and reports the data owner. You have to create a 
SQL table like the one in 'db.sql'.

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
import MySQLdb as mdb
import sys
import smtplib
from email.mime.text import MIMEText
import ConfigParser

# DB Configuration
config = ConfigParser.RawConfigParser()
config.read('xmllinkcheck.cfg')
port = config.getint('DB', 'port')
host = config.get('DB', 'host')
user = config.get('DB', 'user')
passwd = config.get('DB', 'pass')
db = config.get('DB', 'db')

# DB Report
try:
	conn = MySQLdb.connect(host=host,port=port, user=user, passwd=passwd, db=db)
    	c = conn.cursor()
    	c.execute('''SELECT *, count(*) as cc 
				FROM entries 
				GROUP BY dataset_id, url
				HAVING 1 < count(*)
				ORDER BY cc DESC
 	''')
    	report = {}
    	rows = c.fetchall()
    	for row in rows:
    		try:
            		report[row[0]]="Dataset with id: "+row[0]+" was found unavailable PDF link "+row[1]+" on "+row[2]+" and "+row[3]
        	except:
            		report[row[0]] = ""

except mdb.Error, e:
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)
finally:    
    if conn:    
        conn.close()

# Report Configuration
sender = config.get('Report','sender')
recipients = config.get('Report', 'recipients').split("\n")
subject = config.get('Report', 'subject')
from_= config.get('Report', 'from')
to_ = config.get('Report', 'to')
smtp = config.get('Report', 'smtp')

# Compose message
mail = """From: """+from_+"""To: """+to_+"""Subject: """+subject+"""\n+"""+message+"""\n"""+str(report)
# Send mail
try:
    smtpObj = smtplib.SMTP(smtp)
    smtpObj.sendmail(sender, receivers, mail)         
    print "Successfully sent email"
except SMTPException:
    print "Error: unable to send email"
