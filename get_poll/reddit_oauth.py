import requests
import csv



def get_login_info():
    
    with open('../login.txt', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='=', quotechar='"')
        
        client_id =     (next(reader))[1] # aka 'personal use script'
        secret_token =  (next(reader))[1] # aka 'token'
        username =      (next(reader))[1]
        password =      (next(reader))[1]
        user_agent =    (next(reader))[1]

    return client_id, secret_token, username, password, user_agent



def get_headers():

    client_id, secret_token, username, password, user_agent = get_login_info()   

    auth = requests.auth.HTTPBasicAuth(client_id, secret_token)
    
    # here we pass our login method (password), username, and password
    data = {'grant_type': 'password',
            'username': username,
            'password': password}
    
    # setup our header info, which gives reddit a brief description of our app
    headers = {'User-Agent': user_agent}
    
    # send our request for an OAuth token
    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=data, headers=headers)
    
    if 'access_token' in res.json():
        
        print("access token obtained")
    
        # convert response to JSON and pull access_token value
        TOKEN = res.json()['access_token']
    
        # add authorization to our headers dictionary
        headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}
    
        ## while the token is valid (~2 hours) we just add headers=headers to our requests
        #requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)
        
        return headers
    
    else:
        
        return None