import json

'''  '''
with open('settings.json') as f:
    file_content = f.read()
    data = json.loads(file_content)

app_name = 'passman alpha'
database = data['database']