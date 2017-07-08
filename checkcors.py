# Python 3.6.1
import base64
import socket
import pymysql
import time

# CORS Server settings
my_host = "CORS-Server-Name.com.my"
username = "registered-username"
password = "registered-password"
port = "2101"

# Generate an encoding of the username:password for the service. The string must be first encoded in ascii to be correctly parsed by the base64.b64encode function.
pwd = base64.b64encode("{}:{}".format(username, password).encode("ascii"))

# The following decoding is necessary in order to remove the b" character that the ascii encoding add. Otherwise said character will be sent to the net and misinterpreted.
pwd = pwd.decode("ascii")

# MySQL/MariaDB database settings
conn = pymysql.connect(host="Server-Host/IP", port=3306, user="username", password="password", database="DB-Name")

# Open MySQL/MariaDB connection
cur = conn.cursor()

# List of CORS stations
# Example format of CORS's station name in text file (new station name at every new line):
# AGKB
# WUHN
# ANA1
# etc...

stnFile = open("cors_station.txt","r")

print("\nChecking Station...\n")

# Counting online and offline CORS stations
countS1 = 0
countS2 = 0

for corsList in stnFile:
	values = corsList.split()
	#print(values[0:])
	header2 =\
	"GET /" + values[0] + " HTTP/1.1\r\n" +\
	"Host " + my_host + "\r\n" +\
	"Ntrip-Version: Ntrip/1.0\r\n" +\
	"User-Agent: ntripPython.py/0.1\r\n" +\
	"Accept: */* " +\
	"Connection: close\r\n" +\
	"Authorization: Basic {}\r\n\r\n".format(pwd)
	#print(header2)
	
	s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s2.connect((my_host,int(port)))
	s2.send(header2.encode("ascii"))
	
	data2 = s2.recv(2048).decode("ascii")
	#print(data2)

  # CORS station status is ONLINE
	if data2.strip() == "ICY 200 OK":
		print("Station " + values[0] + " is Online")
		countS1 = countS1 + 1
		
		# Store into MySQL/MariaDB database. Status = 1 indicate station is Online
		sqlOnline = "UPDATE stations SET status = 1 WHERE station_id = ""\"" + values[0] + "\""
		cur.execute(sqlOnline)
	else:
		print("Station " + values[0] + " is Offline!")
		countS2 = countS2 + 1
		
		# Store into MySQL/MariaDB database. Status = 2 indicate station is Offline
		sqlOffline = "UPDATE stations SET status = 2 WHERE station_id = ""\"" + values[0] + "\""
		cur.execute(sqlOffline)
	
print("\n\nTotal Online: " + str(countS1) + " stations")
print("Total Offline: " + str(countS2) + " stations\n\n")

stnFile.close()

# Close MySQL/MariaDB connection
cur.close()
conn.close()
time.sleep(4)