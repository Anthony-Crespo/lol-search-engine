import requests

# implement response code needed https://developer.riotgames.com/response-codes.html
# https://developer.riotgames.com/static-data.html

API_KEY = ''
default_region = "NA"
# possible bug when in a function a region is misspell
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
    urn = f'/lol/summoner/v4/summoners/by-name/{summoner_name}'
    uri = url + urn
    params = {
        'api_key' : API_KEY
    }
    request = requests.get(uri, params=params)
    return request.json()


def get_total_mastery(encrypted_summoner_id, region):
    """return an int, the total summoner mastery"""
    url = 'https://' + REGION_URL[region]
    urn = f'/lol/champion-mastery/v4/scores/by-summoner/{encrypted_summoner_id}'
    uri = url + urn
    params = {
        'api_key' : API_KEY
    }
    request = requests.get(uri, params=params)
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
    urn = f'/lol/champion-mastery/v4/champion-masteries/by-summoner/{encrypted_summoner_id}'
    uri = url + urn
    params = {
        'api_key' : API_KEY
    }
    request = requests.get(uri, params=params)
    return request.json()


def get_champion_mastery(encrypted_summoner_id, champion_id, region):
    """return a champion mastery stats of specified summoner"""
    url = 'https://' + REGION_URL[region]
    urn = f'/lol/champion-mastery/v4/champion-masteries/by-summoner/{encrypted_summoner_id}/by-champion/{champion_id}'
    uri = url + urn
    params = {
        'api_key' : API_KEY
    }
    request = requests.get(uri, params=params)
    return request.json()


def get_champion_rotations(region):
    """return a champion mastery stats of specified summoner
    {
        'freeChampionIds': [2, 4, 8, 22, 32, 53, 78, 89, 102, 113, 133, 141, 157, 222], 
        'freeChampionIdsForNewPlayers': [18, 81, 92, 141, 37, 238, 19, 45, 25, 64], 
        'maxNewPlayerLevel': 10
    }
    """
    url = 'https://' + REGION_URL[region]
    urn = f'/lol/platform/v3/champion-rotations'
    uri = url + urn
    params = {
        'api_key' : API_KEY
    }
    request = requests.get(uri, params=params)
    return request.json()


# When season begins put the get_leagues function in place
# https://developer.riotgames.com/api-methods/#league-v4


def lol_status(region):
    """Server info & status"""
    url = 'https://' + REGION_URL[region]
    urn = '/lol/status/v3/shard-data'
    uri = url + urn
    params = {
        'api_key' : API_KEY
    }
    request = requests.get(uri, params=params)
    return request.json()


# there is more match-v4
# possibility to filter by endtime, timstamp
# add error message when no result like when wrong season provided
def get_match_history(accountId, region, champion = False, queue = False, season = False):
    """return match history with optional filter
    champion[int]: Set of champion IDs for filtering the matchlist.
    queue[int]: Set of queue IDs for filtering the matchlist. (420 for rank, 400 for normal)
    season[int]: Set of season IDs for filtering the matchlist.

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
    urn = f'/lol/match/v4/matchlists/by-account/{accountId}'
    uri = url + urn
    params = {
        'champion' : '',
        'queue' : '',
        'season' : '',
        'api_key' : API_KEY
    }
    request = requests.get(uri, params=params)
    return request.json()


def get_match(matchId, region):
    """ return specific match complete data
    {
        gameId: 2966195073,
        platformId: "NA1",
        gameCreation: 1548956679286,
        gameDuration: 2320,
        queueId: 420,
        mapId: 11,
        seasonId: 11,
        gameVersion: "9.2.261.2172",
        gameMode: "CLASSIC",
        gameType: "MATCHED_GAME",
        teams: [
            {
                teamId: 100,
                win: "Fail",
                firstBlood: true,
                firstTower: false,
                firstInhibitor: false,
                firstBaron: false,
                firstDragon: false,
                firstRiftHerald: false,
                towerKills: 2,
                inhibitorKills: 0,
                baronKills: 0,
                dragonKills: 0,
                vilemawKills: 0,
                riftHeraldKills: 0,
                dominionVictoryScore: 0,
                bans: [
                    {
                    championId: 122,
                    pickTurn: 1
                    },
                    {...}
                ]
            },
            {...} # second team
        ],
        participants: [
            {
                participantId: 1,
                teamId: 100,
                championId: 157,
                spell1Id: 14,
                spell2Id: 4,
                # stats contain object like: win::bool, item0 to item6, killingSprees, 
                # totalDamageDealt, firstTowerAssist... for a total of 104 stats
                stats: {},
                # collection of stats in different time of the game
                timeline: {
                    participantId: 1,
                    creepsPerMinDeltas: {
                        10-20: 3.2,
                        0-10: 5.1,
                        30-end: 4,
                        20-30: 4.4
                    },
                    xpPerMinDeltas: {...},
                    goldPerMinDeltas: {...},
                    csDiffPerMinDeltas: {...},
                    xpDiffPerMinDeltas: {...},
                    damageTakenPerMinDeltas: {...},
                    damageTakenDiffPerMinDeltas: {...},
                    role: "SOLO",
                    lane: "MIDDLE"
                }
            },
            {...}
        ],
        participantIdentities: [
            {...},
            {
                participantId: 2,
                player: {
                    platformId: "NA1",
                    accountId: "MJxiqoVNpc9tLuun_0WcVHMdieivMMgYtR-XGTffbOmkUw",
                    summonerName: "Make Out HiIl",
                    summonerId: "gU6uRQTiPoE3MZpIXPR04LIuxq38e-twK-B6oMFeQ-cngck",
                    currentPlatformId: "NA1",
                    currentAccountId: "MJxiqoVNpc9tLuun_0WcVHMdieivMMgYtR-XGTffbOmkUw",
                    matchHistoryUri: "/v1/stats/player_history/NA1/46212752",
                    profileIcon: 2072
                }
            },
            {...}
        ]
    }
    """
    url = 'https://' + REGION_URL[region]
    urn = f'/lol/match/v4/matches/{matchId}'
    uri = url + urn
    params = {
        'api_key' : API_KEY
    }
    request = requests.get(uri, params=params)
    return request.json()


# SPECTATOR-V4


if __name__ == '__main__':
    try:
        print(get_summoner('Make Out Hiil', 'NA')['name'])
        # print(get_total_mastery(summoner['id'], 'NA'))
        # print(get_all_champion_mastery(summoner['id'], 'NA')[2]['chestGranted'])
        # print(get_champion_mastery(summoner['id'], 103, 'NA')['championLevel'])
        # print(get_champion_rotations('NA'))
        # print(lol_status('NA'))
        # print(get_match_history(summoner['accountId'], 'NA', champion = '2', queue = '1', season = '11'))
        print(get_match('2966195073', 'NA'))
        
    except KeyError:
        print('Wrong or expired key')