#! /usr/bin/python
import sys

import requests
import json
from datetime import datetime, timedelta
import os

api_key = os.getenv('API_KEY')
token = os.getenv('TOKEN')
credentials = 'key=[[' + api_key + ']]&token=[[' + token
request_template = """https://api.trello.com/1/{}&""" + credentials
time_est_field_id = os.getenv('TIME_EST_FIELD')


# Get user boards
def get_boards(member_id):
    # req = 'members/' + member_id + '/boards'
    # url = request_template.format(req)
    url = 'https://api.trello.com/1/members/' + member_id + '/boards'
    querystring = {"filter":"starred","fields":"id,name","lists":"none","memberships":"none","organization":"false","organization_fields":"all","key":api_key,"token":token}
    response = requests.request("GET", url, params=querystring)
    print(response.text)


def get_cards(board_id):
    url = 'https://api.trello.com/1/board/' + board_id + '/cards'
    querystring = {"fields":"name,due","members":"false","customFieldItems":"true","key":api_key,"token":token}
    response = requests.request("GET", url, params=querystring)
    all_cards = json.loads(response.text)
    due_cards = list(filter(lambda card: card['due'] is not None, all_cards))
    return due_cards


def sort_cards(due_cards):
    sorted_tasks = sorted(
        due_cards,
        key=lambda card: datetime.strptime(card['due'], '%Y-%m-%dT%H:%M:%S.%fZ'), reverse=False
    )
    return sorted_tasks


def print_cards(tasks):
    print('____________________________________________________________________________')
    print('TASK LIST:')
    print('____________________________________________________________________________')
    print()
    for i in range(len(tasks)):
        print(tasks[i]['name'])
        print('DUE: ' + datetime.strptime(tasks[i]['due'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%c") + ' UTC')
        time_est = get_time_estimate(tasks[i])
        hours = time_est / 60
        if hours < 1:
            print('TIME ESTIMATE: ' + str(time_est) + ' minutes')
        else:
            print('TIME ESTIMATE: ' + str(hours) + ' hours')
        print()
    print('____________________________________________________________________________')
    print()


def get_cards_for_days(tasks, days):
    limit = datetime.utcnow() + timedelta(days=days)
    relevant_cards = list(filter(lambda card: datetime.strptime(card['due'], '%Y-%m-%dT%H:%M:%S.%fZ') <= limit, tasks))
    return relevant_cards


def get_time_estimate(task):
    if len(task['customFieldItems']) > 0:
        return int(next(field for field in task['customFieldItems'] if field['idCustomField'] == time_est_field_id)['value']['number'])
    else:
        return 0


def get_total_time_estimate(tasks):
    total = 0
    for task in tasks:
        time_est = get_time_estimate(task)
        total += time_est
    hours = total / 60
    if hours < 1:
        print('Total time for ' + str(len(tasks)) + ' tasks: ' + str(total) + ' minutes')
    else:
        print('Total time for ' + str(len(tasks)) + ' tasks: ' + str(hours) + ' hours')
    return total


# CLI accessible functions
def get_tasks_for_days(days):
    print('Getting all tasks for next " + days + "days...')
    cards = get_cards(os.getenv('BOARD_ID'))
    incoming_cards = get_cards_for_days(cards, int(days))
    print_cards(sort_cards(incoming_cards))
    print('For next ' + days + ' days:')
    get_total_time_estimate(incoming_cards)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        globals()[sys.argv[1]](sys.argv[2])
    elif len(sys.argv) == 2:
        globals()[sys.argv[1]]
    else:
        cards = get_cards(os.getenv('BOARD_ID'))
        print_cards(sort_cards(cards))
        get_total_time_estimate(cards)
