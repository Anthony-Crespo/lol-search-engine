from apis.RiotApi import RiotApi

riot_api = RiotApi(
    api_key='RGAPI-63c4eddd-ab53-404f-be10-d43cae4d92fd', 
    region="NA"
)

# CHANGE TO MAKE:
# to save api ressource dont generate unimportant object var value yet
# but when the value is first acceded (grouped by api request)
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

player = Summoner('player')
print(player.summoner_level)
print(player.mastery_score)
