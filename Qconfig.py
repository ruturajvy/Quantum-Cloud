# --------------------------------------------------------------------------------
# Before you can use the jobs API, you need to set up an access token.
# Log in to the Quantum Console through https://q-console.mybluemix.net/#/ibmq/ using 
# your IBM ID. Click on "Get Access" in the upper left corner, and generate a
# access token. 
# Replace '_ENTER_TOKEN_HERE_' with your own API token (put it within quotes)
#Enter appropriate entries for hub/group/project and verify the entry for url
# --------------------------------------------------------------------------------

APItoken = '_ENTER_TOKEN_HERE_'

config = {
    "url": 'https://q-console-api.mybluemix.net/api',
    'hub': 'ibmq',
    'group': '_ENTER_GROUP_HERE',
    'project': '_ENTER_PROJECT_HERE'
}

if 'APItoken' not in locals():
    raise Exception('Please set up your access token. See Qconfig.py.')
