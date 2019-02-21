from apis import RiotApi
from apis import SummonerNameInvalid, SummonerNotFound
from requests import HTTPError

try:
    riot_api = RiotApi(
        api_key='RGAPI-802113b9-a5ea-4f2c-8ce4-c7df1dee1b9d', 
        region="NA"
    )
except TypeError:
    pass  # key can only be a string in set_api_key()
except KeyError:
    pass  # region not in dict

# CHANGE TO MAKE:
# to save api ressource dont generate unimportant object var value yet
# but when the value is first acceded (grouped by api request)
    # maybe use @property to acces value and if its empty just create it
class Summoner():
    """Summoner class is created from RiotApi request to Riot official Api"""
    def __init__(self, summoner_name, region = riot_api.default_region):
        # need a try block for not found summoner
        summoner_data = riot_api.get_summoner(summoner_name, region)
        self.id = summoner_data['id']
        self.name = summoner_data['name']
        self.profile_icon_id = summoner_data['profileIconId']
        self.revision_date = summoner_data['revisionDate']
        self.summoner_level = summoner_data['summonerLevel']

        self.mastery_score = riot_api.get_total_mastery(self.id)

try:
    player = Summoner('pla2k33e3kebjyer')
    print(player.summoner_level)
    print(player.mastery_score)
except SummonerNameInvalid:
    pass
except SummonerNotFound:
    pass
except NameError:
    pass
except HTTPError:
    pass
