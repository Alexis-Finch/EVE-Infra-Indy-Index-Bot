import operator
import os
import requests
import json

# Author: Alexis Finch
# Date: July 7, 2023
#
# The purpose of this program is to present a list of cost indexes for Manufacturing and Reactions for an alliance (or alliances) in EVE Online
# The data can then be sent to Discord or Slack
#
# Set it up on a CRON job or task scheduler to cycle regularly, and it'll keep you up to date on the cost indexes in your systems! 


# Formats indexes for sake of readability. Converts decimals into percentages.
def indexFormatter (index):
    return f"{index:.2%}"

#Gets a system id (int)
#Returns a system name (string)
def getNameBySystemID (solar_system_id):
    system_url = 'https://esi.evetech.net/latest/universe/systems/' + repr(solar_system_id)
    return requests.get(system_url).json()["name"]

def GetIndices(alliance_IDs):
    sov_url = 'https://esi.evetech.net/latest/sovereignty/structures/'
    indices_url = 'https://esi.evetech.net/latest/industry/systems/'

    sov_response = requests.get(sov_url).json()

    alliance_systems = []

    for system in sov_response:
        if system['alliance_id'] in alliance_IDs and system['structure_type_id'] == 32458:
            alliance_systems.append(system['solar_system_id'])

    index_response = requests.get(indices_url).json()


    # Stores the data that will be sent at the end
    alliance_indexes_lists = [{'name':'Manufacturing','data':[]},{'name':'Reactions', 'data':[]}]

    #Reads through all indexes returned by ESI
    for cost_index in index_response:
        #Then checks the list of system IDs in the alliance systems list, to see if it's on the list
        for system in alliance_systems:
            # If the systems match (cost index pertains to a system on the alliance_systems list
            if cost_index['solar_system_id'] == system:
                # then it adds the indices to the output data, formatted with system ID and cost index
                alliance_indexes_lists[0]['data'].append({'solar_system_id':cost_index['solar_system_id'], 'cost_index':cost_index['cost_indices'][0]['cost_index']})
                alliance_indexes_lists[1]['data'].append({'solar_system_id':cost_index['solar_system_id'], 'cost_index':cost_index['cost_indices'][5]['cost_index']})


    # Sorts the lists into ascending order
    alliance_indexes_lists[0]['data'] = sorted(alliance_indexes_lists[0]['data'], key=operator.itemgetter('cost_index'))
    alliance_indexes_lists[1]['data'] = sorted(alliance_indexes_lists[1]['data'], key=operator.itemgetter('cost_index'))


    #Reverses the lists of indexes to descending order
    alliance_indexes_lists[0]['data'].reverse()
    alliance_indexes_lists[1]['data'].reverse()

    #String for the final output
    output_string = ""

    #runs through the finalized data, each one is a different index type
    for list in alliance_indexes_lists:
        #add the header to the output
        output_string += (list['name'] + " Cost Index Report: ```")
        # add each systems data
        for system in list['data']:
            if system['cost_index'] > 0.001:
                output_string += (getNameBySystemID(system["solar_system_id"]) + ": " + str(indexFormatter(system['cost_index'])) + "\n")
        # Add the end syntax for the list of systems
        output_string += "```\n\n"

    #if the config file is true for slack
    if configuration['webhooks']['slack']:
        #Pulls the slack URL from the ENV Variable
        slack_url = os.environ["INDY_BOT_SLACK_WEBHOOK_URL"]

        #Sends it in the proper format, to the slack webhook
        requests.post(slack_url, data=json.dumps({'text': output_string}), headers={'Content-Type': 'application/json'})

    #if the config file is true for discord
    if configuration['webhooks']['discord']:
        #Pulls the discord webhook URL from the ENV variable
        discord_url = os.environ['INDY_BOT_DISCORD_WEBHOOK_URL']

        #Sends it in the proper format, to the discord webhook
        requests.post(discord_url, data=json.dumps({'content': output_string}), headers={'Content-Type': 'application/json'})

#opens config file
configFile = open("./config.json")

#returns JSON object as a dictionary
configuration = json.load(configFile)

#Calls the function to fetch, and send, the indexes
GetIndices(configuration["alliance_IDs"])
