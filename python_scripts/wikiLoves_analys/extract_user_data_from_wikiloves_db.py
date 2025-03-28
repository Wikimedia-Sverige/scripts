# extract the user data for later
# the data comes from the wikiloves dump https://wikiloves.toolforge.org/db.json
import json
COUNTRY = 'Sweden'

users = {}

with open("db.json", encoding='utf-8') as f:
    data = json.load(f)

for competition, comp_data in data.items():
    if COUNTRY in comp_data.keys():
        for user, user_data in comp_data[COUNTRY].get('users').items():
            if not user in users:
                users[user] = {
                    'competitions':[],
                    'count':0,
                    'reg':user_data.get('reg'),
                    'recruited': None}
            users[user]['competitions'].append(competition)
            users[user]['count'] += user_data.get('count')
            if comp_data[COUNTRY].get('start') < user_data.get('reg') < comp_data[COUNTRY].get('end'):
                users[user]['recruited'] = competition

with open("db_users.json", "w", encoding="utf-8") as f:
    _ = f.write(json.dumps(users, sort_keys=True, indent=2))
