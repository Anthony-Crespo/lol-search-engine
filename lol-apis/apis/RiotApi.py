import requests
from .errors import notOk, SummonerNameInvalid
from .validators import summoner_name_valid

REGION_URL = {
            'BR': 'https://br1.api.riotgames.com',
            'EUNE': 'https://eun1.api.riotgames.com',
            'EUW': 'https://euw1.api.riotgames.com',
            'JP': 'https://jp1.api.riotgames.com',
            'KR':	'https://kr.api.riotgames.com',
            'LAN':	'https://la1.api.riotgames.com',
            'LAS':	'https://la2.api.riotgames.com',
            'NA':	'https://na1.api.riotgames.com',
            'OCE':	'https://oc1.api.riotgames.com',
            'TR': 'https://tr1.api.riotgames.com',
            'RU':	'https://ru.api.riotgames.com',
            'PBE': 'https://pbe1.api.riotgames.com'
        }


class RiotApi:
    """RiotApi class the main point to request data from Riot official API"""
    def __init__(self, api_key: str, region: str):
        self.api_key = ""
        self.default_region = ""
        
        self.set_api_key(api_key)
        self.set_region(region)

    def set_api_key(self, key: str):
        """Set the API key inside RiotApi class

        Args:
            key (str): Your Riot API key
        Raises:
            TypeError: if key is not a string.

        """
        if isinstance(key, str):
            self.api_key = key
        else:
            raise TypeError('The Riot API key can only be a string')

    def set_region(self, region: str):
        """Set default region for request from the 12 available in Riot API
        (BR, EUNE, EUW, JP, KR, LAN, LAS, NA, OCE, TR, RU, PBE)

        Args:
            region (str): region abreviation representing regional endpoints
        Raises:
            KeyError: if region string don't match with one of REGION_URL key.

        """
        if region in REGION_URL:
            self.default_region = region
        else:
            raise KeyError("There is no such region available.")

    def request_api(self, func):
        """The wrapper aka decorator function for requests"""
        pass

    # Possibility to implement search by account ID, PUUID, summoner ID
    def get_summoner(self, name: str, region: str = ''):
        """SUMMONER-V4 on Riot API (More in Riot official docs)

        Get a summoner by summoner name.

        Args:
            name (str):  summoner name to search data for
            region (str): region abreviation representing regional endpoints
        Returns: 
            SummonerDTO the JSON response (dict) representing a summoner
        Raises:
            Customs errors from notOk : if response status code not 200

        """
        # add 'if region not in REGION_URL' for bad region value to test
        if not region:
            region = self.default_region
        if not summoner_name_valid(name):
            raise SummonerNameInvalid(
                "Summoner name contain invalid characters"
            )

        url = REGION_URL[region] + '/lol/summoner/v4/summoners/by-name/' + name
        params = {
            'api_key' : self.api_key
        }
        response = requests.get(url, params=params)
        notOk(response)
        return response.json()

    def get_total_mastery(self, summoner_id, region: str = ''):
        """CHAMPION-MASTERY-V4 on Riot API (More in Riot official docs)
        
        Get a player's total champion mastery score, which is the sum of 
        individual champion mastery levels.

        Args:
            name (str):  encrypted summoner id
            region (str): region abreviation representing regional endpoints
        Returns: 
            return an int, the summoner total champion mastery score
        Raises:
            Customs errors from notOk : if response status code not 200

        """
        # add 'if region not in REGION_URL' for bad region value to test
        if not region:
            region = self.default_region

        url = REGION_URL[region] + '/lol/champion-mastery/v4/scores/by-summoner/' + summoner_id
        params = {
            'api_key' : self.api_key
        }
        response = requests.get(url, params=params)
        notOk(response)
        return response.json()
