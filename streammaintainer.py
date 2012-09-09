import sys,re,urllib2,time,datetime

#################################################################
# File: streammaintainer.py					#
# Author: Rommel Rico						#
# Last Modified: 9/Sept/2012					#
# Description: 	A small Python script that maintains 		#
# 		a list of live TwitchTV streams on sc2mx.com.	#
#################################################################

#GLOBAL VARIABLES
DIR = '/home/romri/webapps/sc2mx_home/'
EMBED_FILE = 'get_embed.php'
CORE_JS_FILE = 'assets/js/core.js'

#Main function
def main(argv):
	if len(argv) < 2:
		print "Instructions: "
		print " ADD a stream: 		streammaintainer.py -a <StreamName>"
		print " REMOVE a stream: 	streammaintainer.py -r <StreamName>"
		print " MAINTAIN stream list: 	streammaintainer.py -m"
		print " LIST all streams: 	streammaintainer.py -l"
	elif argv[1]=="-a":
		if argv[2]!=None: add(argv[2])
	elif argv[1]=="-r":
		if argv[2]!=None: remove(argv[2])
	elif argv[1]=="-m":
		maintain()
	elif argv[1]=="-l":
		streamList = list()
		for i in streamList:
			print i

#This function adds a single stream.
def add(stream_name):
	#Process first file.
	f1 = open(DIR+EMBED_FILE, 'r')
        strings1 = re.sub(r'(?<=allowed_channels = array\()', '\''+stream_name+'\', ', f1.read())
        f1.close()
        f1 = open(DIR+EMBED_FILE, 'w')
        f1.write(strings1)
        f1.close()
        #Process second file
        f2 = open(DIR+CORE_JS_FILE, 'r')
        strings2 = re.sub(r'(?<=  streamers = \[)', '\''+stream_name+'\', ', f2.read())
        f2.close()
        f2 = open(DIR+CORE_JS_FILE, 'w')
        f2.write(strings2)
        f2.close()
	
#This function removes a single stream.
def remove(stream_name):
	#Process first file.
	f1 = open(DIR+EMBED_FILE, 'r')
	strings1 = re.sub(r'\''+stream_name+'\'[,\s]*', '', f1.read())
	f1.close()
	f1 = open(DIR+EMBED_FILE, 'w')
	f1.write(strings1)
	f1.close()
	#Process second file
	f2 = open(DIR+CORE_JS_FILE, 'r')
	strings2 = re.sub(r'\''+stream_name+'\'[,\s]*', '', f2.read())
	f2.close()
	f2 = open(DIR+CORE_JS_FILE, 'w')
	f2.write(strings2)
	f2.close()
	
#This function removes streams that have not broadcasted content in 30 days.
def maintain():
	streamList = list()	
	for i in streamList:
		days = daysSinceLastStream(i)
		if days > 30:
			remove(i)
		time.sleep(4)   #Wait a few seconds because of TwitchTV's API rate-limits.
	
#Returns a list with all the streams in sc2mx.com.
def list():
	streamList = []
	f = open(DIR+EMBED_FILE, 'r')	#Open file.
	strings = re.findall(r'(?<=allowed_channels = array\()\'.*\'', f.read())
	f.close()			#Close file.
	strings = "".join(strings).replace("\'", "").split(',')
	for i in strings:
		streamList.append(i.strip())
	return streamList

#Returns the number of days a stream last broadcasted on TwitchTV.
def daysSinceLastStream(stream_name):
	today = datetime.date.today()
	url = "http://api.justin.tv/api/channel/archives/"+stream_name+".json?limit=1"
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	date = re.search(r'\d{4}-\d{2}-\d{2}', response.read())
	if date!=None:
		date = date.group(0).split('-')
	else:
		date = ['2001', '01', '01']
	for i in range(len(date)):
		date[i] = int(date[i])
	someday = datetime.date(date[0], date[1], date[2])
	diff = today - someday
	return diff.days

#Launch program.
if __name__ == "__main__":
	main(sys.argv)

