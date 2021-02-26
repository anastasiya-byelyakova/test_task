"""Gets data from airtables"""

import requests

def get_airtables_data(AIRTABLES_TOKEN='',
                       AIRTABLES_ID=''):

    assert AIRTABLES_ID, print('Please give an id for airtables')
    assert AIRTABLES_TOKEN, print('Please give an token for airtables')

    headers = {
        'Authorization': f'Bearer {AIRTABLES_TOKEN}',
    }

    response = requests.get(f'https://api.airtable.com/v0/{AIRTABLES_ID}/Psychotherapists',
                            headers=headers)

    data = []

    for i in response.json()['records']:
        id = i['id']
        name = i['fields']['Имя']
        methods = ', '.join(i['fields']['Методы'])
        photo = i['fields']['Фотография'][0]['url']
        data.append([id, name, methods, photo])

    return data