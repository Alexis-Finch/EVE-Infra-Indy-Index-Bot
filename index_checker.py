import operator
import os
import requests
import json

def indexFormatter (index):
    return f"{index:.2%}"

def getNameBySystemID (solar_system_id):
    system_url = 'https://esi.evetech.net/latest/universe/systems/' + repr(solar_system_id)
    return requests.get(system_url).json()["name"]

def GetIndices(alliance_id):
    sov_url = 'https://esi.evetech.net/latest/sovereignty/structures/'
    indices_url = 'https://esi.evetech.net/latest/industry/systems/'

    sov_response = requests.get(sov_url).json()

    alliance_systems = []

    for system in sov_response:
        if system['alliance_id'] == int(alliance_id) and system['structure_type_id'] == 32458:
            alliance_systems.append(system['solar_system_id'])

    index_response = requests.get(indices_url).json()



    index_list = [{'name':'Manufacturing','data':[]},{'name':'Reactions', 'data':[]}]

    for index in index_response:
        for system in alliance_systems:
            if index['solar_system_id'] == system:
                index_list[0]['data'].append({'solar_system_id':index['solar_system_id'], 'cost_index':index['cost_indices'][0]['cost_index']})
                index_list[1]['data'].append({'solar_system_id':index['solar_system_id'], 'cost_index':index['cost_indices'][5]['cost_index']})

    index_list[0]['data'] = sorted(index_list[0]['data'], key=operator.itemgetter('cost_index'))
    index_list[1]['data'] = sorted(index_list[1]['data'], key=operator.itemgetter('cost_index'))

    index_list[0]['data'].reverse()
    index_list[1]['data'].reverse()

    output_string = ""
    for list in index_list:
        output_string += (list['name'] + " Cost Index Report: ```")
        for system in list['data']:
            if system['cost_index'] > 0.001:
                output_string += (getNameBySystemID(system["solar_system_id"]) + ": " + str(indexFormatter(system['cost_index'])) + "\n")
        output_string += "```\n\n"

    slack_url = os.environ["INDY_BOT_WEBHOOK_URL"]

    requests.post(slack_url, data=json.dumps({'text': output_string}), headers={'Content-Type': 'application/json'})

GetIndices(os.environ["INDY_BOT_ALLIANCE_ID"])
