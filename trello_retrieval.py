import requests
import json
from datetime import datetime, timedelta
import os

api_key = os.getenv('API_KEY')
token = os.getenv('TOKEN')
credentials = 'key=[[' + api_key + ']]&token=[[' + token
request_template = """https://api.trello.com/1/{}&""" + credentials


# Get user boards
def get_boards(member_id):
    # req = 'members/' + member_id + '/boards'
    # url = request_template.format(req)
    url = 'https://api.trello.com/1/members/' + member_id + '/boards'
    querystring = {"filter":"starred","fields":"id,name","lists":"none","memberships":"none","organization":"false","organization_fields":"all","key":api_key,"token":token}
    response = requests.request("GET", url, params=querystring)
    print(response.text)


def get_cards(board_id):
    # req = 'boards/' + board_id + '/cards'
    url = 'https://api.trello.com/1/board/' + board_id + '/cards'
    querystring = {"fields":"name,due","members":"false","customFieldItems":"true","key":api_key,"token":token}
    response = requests.request("GET", url, params=querystring)
    all_cards = json.loads(response.text)
    # print(all_cards)
    due_cards = list(filter(lambda card: card['due'] is not None, all_cards))
    sorted_tasks = sorted(
        due_cards,
        key=lambda card: datetime.strptime(card['due'], '%Y-%m-%dT%H:%M:%S.%fZ'), reverse=False
    )

    return sorted_tasks


def print_cards(tasks):
    for i in range(len(tasks)):
        print(tasks[i]['name'] + ' - DUE: ' + datetime.strptime(tasks[i]['due'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%c"))
        print(tasks[i]['customFieldItems'])


def get_cards_for_days(tasks, days):
    limit = datetime.now() + timedelta(days=days)
    relevant_cards = list(filter(lambda card: datetime.strptime(card['due'], '%Y-%m-%dT%H:%M:%S.%fZ') <= limit, tasks))
    return relevant_cards


def get_total_time_estimate(tasks):
    total = 0
    hours = 0
    minutes = 0
    for task in tasks:
        time_est = next(field for field in task['customFieldItems'] if field['idCustomField'] == '5deac74aa387e46d08bf6520')
        time_est = time_est['value']['number']
        total += int(time_est)
    hours = total / 60
    minutes = total % 60
    print('Total time for ' + str(len(tasks)) + ' tasks: ' + str(hours) + ' hours ' + str(minutes) + ' minutes')
    return total


if __name__ == "__main__":
    username = os.getenv('USERNAME')
    cards = get_cards(os.getenv('BOARD_ID'))
    get_total_time_estimate(get_cards_for_days(cards, 7))
