import requests
import pandas as pd


#Step 1: When user click button -> redirect user to this link to get authorization
#URL: http://www.strava.com/oauth/authorize?client_id=130686&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=activity:read_all

#Step 2: After user accept authorize -> redirect to this link
#URL to get code http://localhost/exchange_token?state=&code=2cf498325b87a8240df4fdd5b7e1c3bb294e4eb2&scope=read,activity:read_all. 
#With code, get bearer token function to get access token
def get_bearer_token(code: str):
    print(code, 'code ne')
    url = 'https://www.strava.com/oauth/token'
    
    data = {
        'client_id': '130686',
        'client_secret': 'f3a5a01c46f8ef409ac2f857b561ad18463beaa4',
        'code': code,
        'grant_type': 'authorization_code'
    }

    response = requests.post(url, data= data)
    #print(response, 'response')
    data = response.json()
    #print(data.keys())
    access_token = data['access_token']
    return access_token

#Step 3: Get activities from strava through Strava API.

CLIENT_ID = '130686'
CLIENT_SECRET = 'f3a5a01c46f8ef409ac2f857b561ad18463beaa4'
ACCESS_TOKEN = '71076746c757a395485bde37ff924a7fb65bbb06'  

# Strava API URLs
BASE_URL = 'https://www.strava.com/api/v3'

#Function to get activities in one page.
def get_activities(access_token, per_page=30, page=1):
    """
    Fetches a list of activities for the user.
    
    :param access_token: Strava access token.
    :param per_page: Number of activities to retrieve per page (max 200).
    :param page: Page number to fetch.
    :return: List of activities or error message.
    """
    CLIENT_ID = '130686'
    CLIENT_SECRET = 'f3a5a01c46f8ef409ac2f857b561ad18463beaa4'
    BASE_URL = 'https://www.strava.com/api/v3'
    
    url = f"{BASE_URL}/athlete/activities"
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'per_page': per_page, 'page': page}

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()  # Returns a list of activities
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
    
#Function to get all activities loop through all pages. Output is JSON
def get_all_activities(access_token, per_page=30):
    """
    Fetches all activities for the user by iterating over all pages.
    
    :param access_token: Strava access token.
    :param per_page: Number of activities to retrieve per page (max 200).
    :return: List of all activities.
    """
    all_activities = []
    page = 1

    while True:
        activities = get_activities(access_token, per_page=per_page, page=page)
        
        if activities:
            all_activities.extend(activities)
            print(f"Fetched {len(activities)} activities from page {page}")
            
            # If the number of activities returned is less than `per_page`, we reached the last page
            if len(activities) < per_page:
                break
        else:
            break  # Stop if there's an error or no more activities

        page += 1

    return all_activities

#Step 4: Visualize JSON as dataframe
#Function to visualize as dataframe
def json_to_df(activity_data):
    df = pd.DataFrame(data = activity_data)
    return df

#Function to download csv file (optional for check)
#Function Download csv file
def df_to_csv(dataframe):
    dataframe.to_csv('activity_lists_strava_api_total.csv')

if __name__ == "__main__":
    #Step 1: Authorize and get code
    #Step 2: Get Access token
    #get_bearer_token_results = get_bearer_token()
    #print(get_bearer_token_results)
    
    access_token = '71076746c757a395485bde37ff924a7fb65bbb06'
    #Step 3: Get activity from API
    activities = get_activities(access_token, per_page=5, page=1)

    #Step 4: Get all activity 
    #all_activities = get_all_activities(access_token, per_page = 30)

    #Step 5: Check all_activities
    #print(all_activities)

    #Step 6: Visualize as dataframe
    df = json_to_df(activities)
    print(df)
    
    print(activities)





