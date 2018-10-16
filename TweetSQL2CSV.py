from operator import itemgetter
import csv
import math

import csv
import os
import copy
import MySQLdb
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
import operator
import sys
import random


db = MySQLdb.connect(host="kurinji.cs.uiowa.edu",    # your host, usually localhost
                     user="okhalid",         # your username
                     passwd="",  # your password
                     db="demographics",charset='utf8', init_command='SET NAMES UTF8')        # name of the data base
        
cursor=db.cursor()
sql = "select* from tweet2 where location like '%, CO'"      
cursor.execute(sql)
Query=cursor.fetchall()
db.commit()
cursor.close()
db.close()
p=0
with open("tweet2CO.csv", "w") as csv_file:
    writer=csv.writer(csv_file,delimiter=',', lineterminator='\n')
    j=0
    for row in Query:
        p=p+len(row)
        
        writer.writerow(row) 
        j=j+1
        
print(j,p)
j=0
p=0
