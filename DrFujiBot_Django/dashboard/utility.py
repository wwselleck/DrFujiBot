import certifi
import iso8601
import json
import urllib.request as request

CLIENT_ID = 'cnus4j6y1dvr60vkqsgvto5almy5j8'

# The purpose of scrambling the token is mainly to prevent bots from scraping the token from GitHub.
# Please do not use this token for any other purpose than the normal functions of DrFujiBot. Thank you.
def unscramble(scrambled):
    unscrambled = ''
    for i in range(0, 30, 2):
        unscrambled += scrambled[i]
    for i in range(1, 30, 2):
        unscrambled += scrambled[i]
    return unscrambled

def get_twitch_access_token():
    access_token = ''
    access_token_url = 'https://raw.githubusercontent.com/EverOddish/DrFujiBot/master/DrFujiBot_Django/data/access_token.txt'
    try:
        req = request.Request(access_token_url)
        response = request.urlopen(req, cafile=certifi.where())
        access_token = response.read().decode('utf-8')
        access_token = unscramble(access_token)
    except Exception as e:
        print('Exception while retrieving access token: ' + str(e))
    return access_token

def twitch_api_request(url):
    data = None
    try:
        access_token = get_twitch_access_token()
        twitch_request = request.Request(url)
        twitch_request.add_header('Client-ID', CLIENT_ID)
        twitch_request.add_header('Authorization', 'Bearer ' + access_token)
        response = request.urlopen(twitch_request, cafile=certifi.where())
        data = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print('Twitch API exception: ' + str(e))
    return data

def get_stream_start_time():
    from .models import Setting
    start_time = None
    username = Setting.objects.get(key='Twitch Username').value
    if len(username) > 0:
        url = 'https://api.twitch.tv/helix/streams?user_login=' + username
        stream_data = twitch_api_request(url)
        if stream_data and len(stream_data['data']) > 0:
            if 'live' == stream_data['data'][0]['type']:
                start_time = iso8601.parse_date(stream_data['data'][0]['started_at'])

    return start_time

def get_viewer_list():
    from .models import Setting
    viewer_list = []
    username = Setting.objects.get(key='Twitch Username').value
    if len(username) > 0:
        url = 'https://tmi.twitch.tv/group/user/' + username + '/chatters'
        chatters_data = twitch_api_request(url)
        if chatters_data:
            for key in chatters_data['chatters']:
                users = chatters_data['chatters'][key]
                for user in users:
                    viewer_list.append(user)
    return viewer_list
