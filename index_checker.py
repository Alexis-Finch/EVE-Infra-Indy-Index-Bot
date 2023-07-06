import operator
import os
import requests
import json

# Author: Alexis Finch
#
# Date: July 5, 2023
#
# The purpose of this program is to present a list of cost indexes for Manufacturing and Reactions for an alliance (or alliances) in EVE Online
# The data can then be sent to Discord or Slack
#
# Set it up on a CRON job or task scheduler to cycle regularly, and it'll keep you up to date on the cost indexes in your systems!


# Formats indexes for sake of readability. Converts decimals into percentages.
def indexFormatter (index):
    return f"{index:.2%}"

def parseIndicesBySystemList (index_response, alliance_systems):
    indices_list = [[],[]]
    #Reads through all indexes returned by ESI

    for cost_index in index_response:
        #Then checks the list of system IDs in the alliance systems list, to see if it's on the list
        for system in alliance_systems:
            # If the systems match (cost index pertains to a system on the alliance_systems list
            if cost_index['solar_system_id'] == system['id']:

                if cost_index['cost_indices'][0]['cost_index'] > configuration['display_threshold']:
                    indices_list[0].append([system['name'],cost_index['cost_indices'][0]['cost_index']])

                if cost_index['cost_indices'][5]['cost_index'] > configuration['display_threshold']:
                    indices_list[1].append([system['name'],cost_index['cost_indices'][5]['cost_index']])

    # sorts the data
    indices_list[0].sort(key=lambda x: x[1])
    indices_list[0].reverse()

    indices_list[1].sort(key=lambda x: x[1])
    indices_list[1].reverse()

    return indices_list

def buildOutputString (indices_list):
    outputString = 'Manufacturing Cost Index Report: ```'

    for system in indices_list[0]:
        system[1] = indexFormatter(system[1])

        outputString += ('{0:7} {1:>8}'.format(*system)) + "\n"

    outputString += "``` \n"
    outputString += 'Reaction Cost Index Report: ```'

    for system in indices_list[1]:
        system[1] = indexFormatter(system[1])

        outputString += ('{0:7} {1:>8}'.format(*system)) + "\n"
    outputString += "```"

    return outputString

def filterByRegions (alliance_systems):
    inRegionFilteredList = []
    resolve_region_id_url = 'https://esi.evetech.net/latest/universe/regions/'
    resolve_constellation_id_url = 'https://esi.evetech.net/latest/universe/constellations/'

    for region in configuration['regions']:
        regionJSON = requests.get(resolve_region_id_url+str(region)).json()
        for constellation in regionJSON['constellations']:
            constellationJSON = requests.get(resolve_constellation_id_url+str(constellation)).json()
            for system in constellationJSON['systems']:
                for trackedSystem in alliance_systems:
                    if system == trackedSystem['id']:
                        inRegionFilteredList.append(trackedSystem)

    return inRegionFilteredList

def postSlackWebhook (content):
    #Pulls the slack URL from the ENV Variable
    slack_url = os.environ["INDY_BOT_SLACK_WEBHOOK_URL"]

    #Sends it in the proper format, to the slack webhook
    requests.post(slack_url, data=json.dumps({'text': content}), headers={'Content-Type': 'application/json'})

def postDiscordWebhook (content):
    #Pulls the discord webhook URL from the ENV variable
    discord_url = os.environ['INDY_BOT_DISCORD_WEBHOOK_URL']

    #Sends it in the proper format, to the discord webhook
    requests.post(discord_url, data=json.dumps({'content': content}), headers={'Content-Type': 'application/json'})

def GetIndices(alliance_IDs):
    sov_url = 'https://esi.evetech.net/latest/sovereignty/structures/'
    indices_url = 'https://esi.evetech.net/latest/industry/systems/'

    sov_response = requests.get(sov_url).json()

    alliance_systems = []

    for system in sov_response:
        if system['alliance_id'] in alliance_IDs and system['structure_type_id'] == 32458:
            alliance_systems.append(system['solar_system_id'])

    resolve_system_name_url = 'https://esi.evetech.net/latest/universe/names/'
    alliance_systems = requests.post(resolve_system_name_url, headers={'Accept': 'application/json','Content-Type': 'application/json','Cache-Control': 'no-cache'}, json=alliance_systems).json()

    alliance_systems = filterByRegions(alliance_systems)

    index_response = requests.get(indices_url).json()


    system_indices_list = parseIndicesBySystemList(index_response, alliance_systems)

    output_string = buildOutputString(system_indices_list)

    #if the config file is true for slack
    if configuration['webhooks']['slack']:
        postSlackWebhook(output_string)

    #if the config file is true for discord
    if configuration['webhooks']['discord']:
        postDiscordWebhook(output_string)

#opens config file
configFile = open("./config.json")

#returns JSON object as a dictionary
configuration = json.load(configFile)

#Calls the function to fetch, and send, the indexes
GetIndices(configuration["alliance_IDs"])
