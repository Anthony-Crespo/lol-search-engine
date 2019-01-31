import requests

# implement response code needed https://developer.riotgames.com/response-codes.html
# https://developer.riotgames.com/static-data.html

API_KEY = 'RGAPI-95f5d4be-f544-40fc-9610-16e3e589a7dd'
REGION_URL = {
    'BR': 'br1.api.riotgames.com',
    'EUNE': 'eun1.api.riotgames.com',
    'EUW': 'euw1.api.riotgames.com',
    'JP': 'jp1.api.riotgames.com',
    'KR':	'kr.api.riotgames.com',
    'LAN':	'la1.api.riotgames.com',
    'LAS':	'la2.api.riotgames.com',
    'NA':	'na1.api.riotgames.com',
    'OCE':	'oc1.api.riotgames.com',
    'TR': 'tr1.api.riotgames.com',
    'RU':	'ru.api.riotgames.com',
    'PBE': 'pbe1.api.riotgames.com'
}
CHAMPIONS = requests.get('http://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/champion.json').json()


# There is a possibility to implement search by account ID, PUUID, summoner ID
def get_summoner(summoner_name, region):
    """ return a dict object with summoner where id's are crypted
    {
        id: "gU6uRQTiPoE3MZpIXPR04LIuxq38e-twK-B6oMFeQ-cngck",
        accountId: "MJxiqoVNpc9tLuun_0WcVHMdieivMMgYtR-XGTffbOmkUw",
        puuid: "7KtgXoWhFMQIjWRMbIVDjeh1XG2FFJLzCnFRnX0IFdimUQIdJziSL6DB6j-lCZ17KyeGYq0PubitlA",
        name: "Make Out HiIl",
        profileIconId: 2072,
        revisionDate: 1548341978000,
        summonerLevel: 146
    }
    """
    url = 'https://' + REGION_URL[region]
    urn = f'/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={API_KEY}'
    uri = url + urn
    request = requests.get(uri)
    return request.json()


def get_total_mastery(encrypted_summoner_id, region):
    """return an int, the total summoner mastery"""
    url = 'https://' + REGION_URL[region]
    urn = f'/lol/champion-mastery/v4/scores/by-summoner/{encrypted_summoner_id}?api_key={API_KEY}'
    uri = url + urn
    request = requests.get(uri)
    return request.json()


def get_all_champion_mastery(encrypted_summoner_id, region):
    """ return all champions mastery stats of specified summoner
    [
        {
        championId: 103,
        championLevel: 7,
        championPoints: 213991,
        lastPlayTime: 1531973501000,
        championPointsSinceLastLevel: 192391,
        championPointsUntilNextLevel: 0,
        chestGranted: false,
        tokensEarned: 0,
        summonerId: "gU6uRQTiPoE3MZpIXPR04LIuxq38e-twK-B6oMFeQ-cngck"
        },
        {...}
    ]
    """
    url = 'https://' + REGION_URL[region]
    urn = f'/lol/champion-mastery/v4/champion-masteries/by-summoner/{encrypted_summoner_id}?api_key={API_KEY}'
    uri = url + urn
    request = requests.get(uri)
    return request.json()


def get_champion_mastery(encrypted_summoner_id, champion_id, region):
    """return a champion mastery stats of specified summoner"""
    url = 'https://' + REGION_URL[region]
    urn = f'/lol/champion-mastery/v4/champion-masteries/by-summoner/{encrypted_summoner_id}/by-champion/{champion_id}?api_key={API_KEY}'
    uri = url + urn
    request = requests.get(uri)
    return request.json()


def champion_rotations(region):
    """return a champion mastery stats of specified summoner
    {
        'freeChampionIds': [2, 4, 8, 22, 32, 53, 78, 89, 102, 113, 133, 141, 157, 222], 
        'freeChampionIdsForNewPlayers': [18, 81, 92, 141, 37, 238, 19, 45, 25, 64], 
        'maxNewPlayerLevel': 10
    }
    """
    url = 'https://' + REGION_URL[region]
    urn = f'/lol/platform/v3/champion-rotations?api_key=' + API_KEY
    uri = url + urn
    request = requests.get(uri)
    return request.json()


# When season begins put the get_leagues function in place
# https://developer.riotgames.com/api-methods/#league-v4


def lol_status(region):
    """Server info & status"""
    url = 'https://' + REGION_URL[region]
    urn = '/lol/status/v3/shard-data?api_key=' + API_KEY
    uri = url + urn
    request = requests.get(uri)
    return request.json()


# match-v4
# possibility to filter by champion, queu, season, endtime
def get_match_history(accountId, region):
    """return matches history
    
    {
        matches: [
            {
            platformId: "NA1",
            gameId: 2966195073,
            champion: 145,
            queue: 420,
            season: 11,
            timestamp: 1548956679286,
            role: "DUO_CARRY",
            lane: "BOTTOM"
            },
            {...}
        ],
        startIndex: 0,
        endIndex: 100,
        totalGames: 192
    {
    """
    url = 'https://' + REGION_URL[region]
    urn = f'/lol/match/v4/matchlists/by-account/{accountId}?api_key={API_KEY}'
    uri = url + urn
    request = requests.get(uri)
    return request.json()

# SPECTATOR-V4


if __name__ == '__main__':
    try:
        summoner = get_summoner('Make Out Hiil', 'NA')
        print(summoner['name'])

        summoner_mastery = get_total_mastery(summoner['id'], 'NA')
        print(summoner_mastery)

        champions_mastery = get_all_champion_mastery(summoner['id'], 'NA')
        print(champions_mastery[2]['chestGranted'])

        ahri_level = get_champion_mastery(summoner['id'], 103, 'NA')['championLevel']
        print(ahri_level)

        print(champion_rotations('NA'))

        print(get_match_history(summoner['accountId'], 'NA'))
    except KeyError:
        print('Key may be expire')