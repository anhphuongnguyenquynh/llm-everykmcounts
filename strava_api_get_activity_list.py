import requests
import pandas as pd

#get bearer token function -> return get access token
def get_bearer_token():
    url = 'https://www.strava.com/oauth/token'

    data = {
        'client_id': '130686',
        'client_secret': '16248f6e5ec1c49f7856ca09adc67e92bd3ce433',
        'code': 'ada40e409f17111b482dd0e45383b0c32a0a21fb',
        'grant_type': 'authorization_code'
    }

    response = requests.post(url, data= data)
    #print(response, 'response')
    data = response.json()
    #print(data.keys())
    access_token = data['access_token']
    return access_token

#get data from api strava
def get_data_from_strava_api(access_token, parameter):
    header = {
        "Authorization": f"Bearer {access_token}"
        # "Authorization": "Bearer " + access_token
    }
    print(header)
    url = "https://www.strava.com/api/v3/athlete/activities"
    #url = "https://www.strava.com/api/v3/athlete/activities?before=&after=&page=&per_page="
    # parameter = {
    #     'page' : 2
    # }
    response = requests.get(url=url, headers=header, params=parameter) 
    return response.json()

#handle pagination
def get_all_strava_activities(access_token):
    all_activities = []
    page = 1
    per_page = 30  # We'll request 30 activities per page

    while True:
        # Get data for the current page
        parameter = {
            'page': page
        }
        
        activities = get_data_from_strava_api(access_token, parameter)
        
        # Add the activities from this page to our list
        all_activities.extend(activities)
        
        # If less than 30 activities are returned, we've reached the last page
        if len(activities) < per_page:
            break
        
        # Move to the next page
        page += 1
    
    return all_activities

#visualize as dataframe
def read_data(activity_data):
    df = pd.DataFrame(data = activity_data)
    return df

#Download csv file
def df_to_csv(dataframe):
    dataframe.to_csv('activity_lists_strava_api_total.csv')

if __name__ == "__main__":
    #get_bearer_token_results = get_bearer_token()
    #print(get_bearer_token_results)
    access_token = 'f1ec59cd0d0b54fb92b62f4157771010d10fa76d'
    response_api = get_all_strava_activities(access_token=access_token)
    print(response_api)
    response_df = read_data(response_api)
    print(response_df)
    df_to_csv(response_df)


