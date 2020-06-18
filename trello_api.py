import requests

class trello_api(object):

    def __init__(self, key, token):
        self.key = key
        self.token = token

    def create_board(self, board):
        url = 'https://api.trello.com/1/boards/'
        query = {'name': board,
                 'key': self.key,
                 'token': self.token}
        response = requests.request("POST", url, params=query)
        board_id = response.json()["id"]
        short_url = response.json()["shortUrl"]
        return board_id, short_url

    def delete_board(self, board_id):
        query = {'key': self.key,
                 'token': self.token}
        url = 'https://api.trello.com/1/boards/{}'.format(self.board_id)
        response = requests.request("DELETE", url, params=query)
        return response.status_code

    def get_board(self, board_id):
        query = {'key': self.key,
                 'token': self.token}
        url = 'https://api.trello.com/1/boards/{}'.format(self.board_id)
        response = requests.request("GET", url, params=query)
        return response.status_code

    def create_column (self, board_id, column):
        url = 'https://api.trello.com/1/boards/{}/lists'.format(board_id)
        query = {'name': column,
                 'key': self.key,
                 'token': self.token,
                 'idBoard': board_id}
        response = requests.request("POST", url, params=query)
        column_id = response.json()["id"]
        return column_id, response.status_code

    def get_column_name(self, column_id):
        query = {'key': self.key,
                 'token': self.token}
        url = 'https://api.trello.com/1/lists/{}'.format(column_id)
        response = requests.request("GET", url, params=query)
        column_name = response.json()["name"]
        return column_name

    def move_column_top(self, column_id):
        query = {'key': self.key,
                 'token': self.token,
                 'pos': '1'}
        url = 'https://api.trello.com/1/lists/{}'.format(column_id)
        requests.request("PUT", url, params=query)

    def get_card_column(self, board_id, column_name):
        query = {'key': self.key,
                 'token': self.token}
        url = 'https://api.trello.com/1/boards/{}/lists'.format(board_id)
        response = requests.request("GET", url, params=query)
        for list in response.json():
            if list['name'] == column_name:
                return list['id']
        raise RuntimeError('Column {} not found'.format(column_name))

    def get_card_id(self, board_id, card_name, column_name):
        query = {'key': self.key,
                 'token': self.token}
        column_id = trello_api.get_card_column(self, board_id, column_name)
        url = 'https://api.trello.com/1/lists/{}/cards'.format(column_id)
        response = requests.request("GET", url, params=query)
        for card in response.json():
            if card['name'] == card_name:
                return card['id']
        raise RuntimeError('Card {} not found'.format(card_name))

    def create_card (self, list_id, card):
        url = 'https://api.trello.com/1/cards'
        query = {'name': card,
                 'key': self.key,
                 'token': self.token,
                 'idList': list_id}
        response = requests.request("POST", url, params=query)
        card_id = response.json()["id"]
        return card_id, response.status_code

    def get_card_data(self, card_id):
        query = {'key': self.key,
                 'token': self.token}
        url = 'https://api.trello.com/1/cards/{}'.format(card_id)
        response = requests.request("GET", url, params=query)
        card_name = response.json()["name"]
        card_list = response.json()["idList"]
        return card_name, card_list

    def update_card (self, card_id, **kwargs):
        url = 'https://api.trello.com/1/cards/{}'.format(card_id)
        query = {'key': self.key,
                 'token': self.token,
                 'idCard': card_id}
        name = kwargs.get('name')
        idList = kwargs.get('idList')
        if name:
            query['name']= name
        if idList:
            query['idList']= idList
        response = requests.request("PUT", url, params=query)
        return response.status_code
