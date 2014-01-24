xmllinkcheck
==============

*Two scripts to check link availability in XML files and generate appropriate reports.*

*Version: Beta 0.1*

xmllinkcheck.py
--------------

Checks for link availability within XML documents and saves the url 
and the timestamp of the checking into the database.

* ./xmllinkcheck.py \<xmlfile\>

gen_report.py
--------------

Checks for two unavailability entries in the DB for in less 
than a month and reports the data owner. You have to create a 
SQL table like the one in 'db.sql'.

* ./gen_report.py

db.sql
--------------

Creates the table. The database must be created already.

xmllinkcheck.cfg
--------------

Configuration file. You have to provide everything.

Author & License
--------------
Author: Jaakko Lappalainen, 2014. email: jkk.lapp@gmail.com

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

