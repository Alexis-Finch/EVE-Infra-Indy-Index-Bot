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

    # Stores the data that will be sent at the end
    alliance_indexes_lists = [{'name':'Manufacturing','data':[]}, {'name':'TE Research', 'data':[]}, {'name':'ME Research','data':[]}, {'name':'Copying','data':[]},{'name':'Invention','data':[]},{'name':'Reactions', 'data':[]}]



    #Reads through all indexes returned by ESI
    for cost_index in index_response:
        #Then checks the list of system IDs in the alliance systems list, to see if it's on the list
        for system in alliance_systems:
            # If the systems match (cost index pertains to a system on the alliance_systems list
            if cost_index['solar_system_id'] == system['id']:
                # then it adds the indices to the output data, formatted with system ID and cost index

                for list in enumerate(alliance_indexes_lists):
                    if configuration['indices'][list[1]['name']]:
                        alliance_indexes_lists[list[0]]['data'].append({'system_name':system['name'], 'cost_index':cost_index['cost_indices'][list[0]]['cost_index']})
                        alliance_indexes_lists[list[0]]['data'] = sorted(alliance_indexes_lists[list[0]]['data'], key=operator.itemgetter('cost_index'))
                        alliance_indexes_lists[list[0]]['data'].reverse()

    return(alliance_indexes_lists)

def buildOutputString (index_data):

    output_string = ""

    #runs through the finalized data, each one is a different index type
    for list in index_data:
        if len(list['data']) > 0:
            #add the header to the output
            output_string += (list['name'] + " Cost Index Report: ```")
            # add each systems data
            for system in list['data']:
                if system['cost_index'] > configuration['display_threshold']:
                 output_string += (system["system_name"] + ": " + str(indexFormatter(system['cost_index'])) + "\n")
            # Add the end syntax for the list of systems
            output_string += "```\n\n"
    return output_string

def parseIndicesBySystemListV2 (index_response, alliance_systems):
    return 1

def buildOutputStringV2 (index_data):
    return 1


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
    resolve_system_name_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache'
    }

    alliance_systems = requests.post(resolve_system_name_url, headers=resolve_system_name_headers, json=alliance_systems).json()

    index_response = requests.get(indices_url).json()

    alliance_indexes_lists = parseIndicesBySystemList(index_response, alliance_systems)

    output_string = buildOutputString(alliance_indexes_lists)

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
