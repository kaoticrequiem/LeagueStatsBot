#!usr/bin/python

import requests
import time
import sys
import argparse
import configparser
import json
import csv

def main(argv):
	# Arguments
	parser = argparse.ArgumentParser(description="Stats Generation Bot")
	parser.add_argument("-o", default = "stats.csv", help="Optional output file.")
   	args = parser.parse_args()
        
    # Read the config file
	config = configparser.ConfigParser()
	config.read('config.ini')
	api_key = config.get('main','apiKey')   

	io = args.o
   	outfile = open(io, "ab+")

	# Build .csv
	data = csv.writer(outfile, quotechar='"', delimiter=',', dialect='excel',
		quoting=csv.QUOTE_MINIMAL, skipinitialspace=True)
	header = ["Total Damage", "Game Created", "Game ID"]
	data.writerow(header)

	retrieve_stats = requests.get('https://na.api.pvp.net/api/lol/na/v1.3/stats/by-summoner/23928317/ranked?season=SEASON2016&api_key=' + api_key)
	retrieve_champ_id = requests.get('https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion?api_key=' + api_key)
	retrieve_game_stats = requests.get('https://na.api.pvp.net/api/lol/na/v1.3/game/by-summoner/23928317/recent?api_key=' + api_key)
	iteration = 0


	# Check the response code for the API requests.
	print "The status code for Champion Stats is " + str(retrieve_stats.status_code)
	print "The status code for Game Stats is " +str(retrieve_game_stats.status_code)


	# Extract the JSON data from the API requests.
	if retrieve_stats.status_code == 200:
		stats_json = retrieve_stats.json()
		total_damage = []
		#print "The URL for the request is %s" % str('https://na.api.pvp.net/api/lol/na/v1.3/stats/by-summoner/23928317/ranked?season=SEASON2016&api_key=' + api_key)
		for champion in stats_json['champions']:
			total_damage = champion['stats']['totalDamageDealt']
			if total_damage != 0:
				print "The total damage is " + str(total_damage)
			else:
				print "Total damage is a null value."
	else:
		print "Something went wrong!"

	if retrieve_game_stats.status_code == 200:
		games_stats_json = retrieve_game_stats.json()
		total_damage = []
		create_date = []
		game_id = []
		#print "The URL for the request is %s" % str('https://na.api.pvp.net/api/lol/na/v1.3/game/by-summoner/23928317/recent?&api_key=' + api_key)
		for champion in games_stats_json['games']:
			total_damage = champion['stats']['totalDamageDealt']
			create_date = champion['createDate']
			game_id = champion['gameId']
			human_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(create_date / 1000))
			human_time = str((human_time) + " UTC")
			time_played = long((champion['stats']['timePlayed']) / 60)
			winner_winner = champion['stats']['win']
			'''if total_damage != 0:
				iteration = iteration + 1
				print "The total damage is " + str(total_damage)
				print "The time this game was created in human terms is " + human_time
				print "The iteration value is " + str(iteration)
				print "The time played is " + str(time_played)
			else:
				print "Total damage is a null value."
			if winner_winner:
				print "You won this game!"
			else:
				print "You lost this game. :(" '''
			output = [total_damage, human_time, game_id]
			data.writerow(output)
			'''
			print rowscan
			print table
			for row in rowscan:
				print "Testing to see if we're in loop."
				break'''
	else:
		print "Something went wrong!"

'''
	if retrieve_champ_id.status_code == 200:
		champid_json = retrieve_champ_id.json()
		for datadict in champid_json['data']:
			idvalue = champid_json['data'][datadict]['id']
			champname = champid_json['data'][datadict]['name']
			print str(champname) + "'s ID value is " + str(idvalue)
'''
'''	
def csv_create(retrieve_game_stats):
	for champion in games_stats_json:
		totaldmg, gamecreate = (" ") * 2
'''

if __name__ == "__main__":
	main(sys.argv[1:])