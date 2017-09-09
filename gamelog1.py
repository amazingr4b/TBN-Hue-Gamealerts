#################################################################
#License and Use Agreement:                                     #
#                                                               #
#Use of the TBN-Gamelog script is at will, and at your own risk.#
#No warranty or support is provided.                            #
#                                                               #
#This script makes use of the Philips Hue API.                  #
#TBN-Gamelog and TheBaconNation are unaffiliated with Philips   #
#Hue.                                                           #
#                                                               #
#The Hue Portions of this script are made possible via          #
#the phue library: https://github.com/studioimaginaire/phue     #
#                                                               #
#TBN-Gamelog, in part and in whole, is for personal use only.   #
#                                                               #
#TBN-Gamelog may not be used in another project without written #
#premission from TheBaconNation.                                #
#################################################################



import time #used for time
import urllib3 #used for http get requests
import re #used for regex action
import os #can be used for os action. For example launching a shell script. 
import sys #used to get gamelink from commandline option
#import tbn_hue #used for hue commands. needs tbn-plex currently. 

#old method
from phue import Bridge #used for hue actions
b = Bridge('192.168.1.126') #bridge ip goes here

#current supported color options
supcolors = ['white','green','red','blue','liteblue','yellow','purple','pink','orange']

#used for the location of the last play log. you need to specify a directory and file in between the "" below
#global LASTPLAYTEXTLINK
#LASTPLAYTEXTLINK = ""

#if enabled, this is used for the game play log. 
#global GAMELOGTEXT
#GAMELOGTEXT = ""

#how long to wait inbetween checks. 
WAIT = 15

#used to make get requests easier. 
http = urllib3.PoolManager()

#what happens when a touchdown is scored. 
def touchdown():
	if HASTHEBALL == 0:
		color = COLOR2
	elif HASTHEBALL == 1:
		color = COLOR1
	else:
		color = "white"
	group = "all"
	
	if color.lower() == "white":
		colcmd = {'transitiontime' : 0, 'on' : True, 'xy' : [0.3804, 0.3768]}
	elif color.lower() == "green":
		colcmd = {'transitiontime' : 0, 'on' : True, 'xy' : [0.4356, 0.4907]}
	elif color.lower() == "red":
		colcmd = {'transitiontime' : 0, 'on' : True, 'xy' : [0.6622, 0.3244]}
	elif color.lower() == "blue":
		colcmd = {'transitiontime' : 0, 'on' : True, 'xy' : [0.1768, 0.0557]}
	elif color.lower() == "liteblue":
		colcmd = {'transitiontime' : 0, 'on' : True, 'xy' : [0.1546, 0.2585]}
	elif color.loewr() == "yellow":
		colcmd = {'transitiontime' : 0, 'on' : True, 'hue' : 10787, 'sat' : 248}
	elif color.lower() == "purple":
		colcmd = {'transitiontime' : 0, 'on' : True, 'hue' : 53124, 'sat' : 254}
	elif color.lower() == "pink":
		colcmd = {'transitiontime' : 0, 'on' : True, 'hue' : 56389, 'sat' : 179}
	elif color.lower() == "orange":
		{'transitiontime' : 0, 'on' : True, 'hue' : 6322, 'sat' : 220}
		
	resetcmd = {'transitiontime' : 0, 'on' : True, 'xy' : [0.3804, 0.3768]}
	'''
	jump = .25
	tbn_hue.setbri(group, 255)
	time.sleep(jump)
	tbn_hue.setbri(group, 75)
	time.sleep(jump)
	tbn_hue.setbri(group, 255)
	time.sleep(jump)
	tbn_hue.setbri(group, 75)
	time.sleep(jump)
	tbn_hue.setlwhite(group)
	tbn_hue.setlwhite(group)
	tbn_hue.setbri(group, 200)
	'''
	GROUP = "All" #light group that reacts to score events. 
	command1 = {'transitiontime' : 0, 'on' : True, 'bri' : 125}
	command2 = {'transitiontime' : 0, 'on' : True, 'bri' : 250}
	jump = .25
	b.set_group(GROUP,colcmd)
	time.sleep(jump)
	b.set_group(GROUP, command1)
	time.sleep(jump)
	b.set_group(GROUP, command2)
	time.sleep(jump)
	b.set_group(GROUP, command1)
	time.sleep(jump)
	b.set_group(GROUP, command2)
	time.sleep(jump)
	b.set_group(GROUP, command1)
	time.sleep(jump)
	b.set_group(GROUP, resetcmd)

#general game function. 
def lastplay(GAMELINK):
	#get game data
	response = http.urlopen('GET', GAMELINK, preload_content=False).read()
	response = str(response)
	lastplay = response
	teams = response
	
	#get teams
	teams = teams.split("<title>")
	teams = teams[1]
	teams = teams.split(" - ")
	teams = teams[0]
	global HASTHEBALL
	if ("team away possession" in response):
		AT = "(HB) at "
		HASTHEBALL = 1
	elif ("team home possession" in response):
		AT = " at (HB)"
		HASTHEBALL = 0
	else:
		AT = " at "
	teams = teams.replace(" vs. ", AT)
	print (teams)
	#get details of last play from previous run. If no previous run, makes file. 
	global LASTPLAYTEXT
	try:
		LASTPLAYTEXT
	except NameError:
		LASTPLAYTEXT = "BLAHBLAHBLAH"
	prevplay = LASTPLAYTEXT
	
	#getting the last play details from the body of the page. 
	lastplay = lastplay.split('<span class="last-down-and-distance lastPlayValue">')
	try:
		lastplay = lastplay[1]
		lastplay = lastplay.split('<div class="content"></div>')
		lastplay = lastplay[0]

		lp1 = lastplay
		lp2 = lastplay
		lp1 = lp1.split('</span><div ')
		lp1 = lp1[0]

		lp2 = lp2.split('class="last-play-text lastPlayDetail">')
		lp2 = lp2[1]
		lp2 = lp2.split('</div></div>')
		lp2 = lp2[0]
		lp2 = lp2.lower()
		
		#checking vs last play
		if (prevplay in lp2):
			say = "No Change in play."
		else:
			lp2 = lp2.lower()
			LASTPLAYTEXT = lp2
			
			#uncomment the next three lines to enable the game log text file.
			'''
			with open(GAMELOGTEXTLINK, "a") as file:
				file.write(lp1 + "\n" + lp2 + "/n/n")
			file.close()'''
		
			if "timeout" in lp2:
				say = "Timeout"
			else:
				#formatting text for reading. Removing unneeded links and extra characters. Etc.	
				alp2 = lp2
				re.sub('\(.*?\)','', alp2)
				ptime = alp2[1]
				ptackle = alp2[2]
				xlp = "Last Play: " + lp1 + "\n" + alp2
				xlp = xlp.replace('(shotgun)', 'From the Shotgun, ')
				xlp = xlp.replace('(no huddle)', 'Using no huddle, ')
				xlp = xlp.replace('(field goal formation)', 'Kicking the field goal, ')

				ptime = xlp
				say = xlp
				lp2 = lp2.lower()
				#show last play details for reference. Can comment out if you dont' care about that. 
				#print (lp2)

				#score checks. 
				if "touchdown" in lp2:
					print("TOUCHDOWN!!")
					touchdown()
					#with open(LASTPLAYTEXTLINK, "w+") as file:
						#file.write("touchdown")
					#file.close()
					#DESIRED TOUCHDOWN ALERT ACTION GOES HERE.
				elif (("field goal" in lp2) or (" yd fg good " in lp2)):
					print ("Field Goal!!!")
					#with open(LASTPLAYTEXTLINK, "w+") as file:
						#file.write("field goal")
					#file.close()
					#DESIRED FIELD GOAL ALERT ACTION GOES HERE.
					touchdown()
				elif "safety" in lp2:
					#with open(LASTPLAYTEXTLINK, "w+") as file:
						#file.write("safety")
					#file.close()
					print ("SAFETY!!!")
					#DESIRED SAFETY ALERT ACTION GOES HERE.
					touchdown()
				elif ("play under review" in lp2):
					print ("The Play is being reviewed!!!")
					#desired review action goes here
	except IndexError:
			finalc = response
			finalc = finalc.split("<div class=\"game-status\">")
			finalc = finalc[1]
			finalc = finalc.split("</span>")
			finalc = finalc[0]
			if ("Final" in finalc):
				say = "This game has ended."
			elif ("network" in finalc):
				say = "This game has not yet started."
	return say

while True:
		
	try:
		try:
			GAMELINK = str(sys.argv[1])
		except IndexError:
			print ("Error: Please supply a game link to proceed.")
		try:
			global COLOR1
			COLOR1 = sys.argv[2]
			if COLOR1.lower() not in supcolors:
				print ("Unsupported Color 1. Using \"white\"")
				COLOR1 = "white"
		except IndexError:
			COLOR1 = "white"
		try:
			global COLOR2
			COLOR2 = sys.argv[3]
			if COLOR2.lower() not in supcolors:
				print ("Unsupported Color 2. Using \"white\"")
				COLOR2 = "white"
		except IndexError:
			COLOR2 = "white"
		say = lastplay(GAMELINK)
		if (say != "No Change in play."):
			print (say)
		if ("This game has ended" in say):
			break
	except (Exception):
		error = "Script Error. Waiting 15 seconds and retrying."
		print (error)
		time.sleep(WAIT)
		continue
	from time import localtime, strftime
	xtime = strftime("%a, %d %b %Y %H:%M:%S +0000", localtime())
	#print (xtime)
	#print ("Waiting for 15 seconds to scan again.")
	time.sleep(WAIT)