import requests
import json
from datetime import datetime
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
    querystring = {"fields":"name,due","members":"false","key":api_key,"token":token}
    response = requests.request("GET", url, params=querystring)
    all_cards = json.loads(response.text)
    # print(all_cards)
    due_cards = list(filter(lambda card: card['due'] is not None, all_cards))
    sorted_tasks = sorted(
        due_cards,
        key=lambda card: datetime.strptime(card['due'], '%Y-%m-%dT%H:%M:%S.%fZ'), reverse=False
    )

    # print(due_cards)
    for i in range(len(sorted_tasks)):
        print(sorted_tasks[i]['name'] + ' - DUE: ' + datetime.strptime(sorted_tasks[i]['due'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%c"))


if __name__ == "__main__":
    username = os.getenv('USERNAME')
    get_boards(username)
    get_cards('5bbe7f8af2edd68b5b21161a')
