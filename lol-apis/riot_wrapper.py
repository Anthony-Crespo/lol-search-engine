from apis import RiotApi
from apis import SummonerNameInvalid, SummonerNotFound, OverRateLimit
from summoners import IntegrityError, Summoner as Summoner_tb
from requests import HTTPError

try:
    riot_api = RiotApi(
        api_key='', 
        region="NA"
    )
except TypeError:
    pass  # key can only be a string in set_api_key()
except KeyError:
    pass  # region not in dict


# Replace this class with the Summoner Model class
class Summoner():
    """Summoner class is created from RiotApi request to Riot official Api"""
    def __init__(self, summoner_name, region = riot_api.default_region):
        # need a try block for not found summoner
        summoner_data = riot_api.get_summoner(summoner_name, region)
        self.id = summoner_data['id']
        self.region = riot_api.default_region
        self.name = summoner_data['name']
        self.profile_icon_id = summoner_data['profileIconId']
        self.revision_date = summoner_data['revisionDate']
        self.level = summoner_data['summonerLevel']

        if not summoner_data_in_db:
            self.mastery_score = riot_api.get_total_mastery(self.id)
        else:
            self.mastery_score = riot_api.get_total_mastery(self.id)


def summoner_data_in_db(summoner: Summoner):
    """Check if a summoner is in the database and up to date
    return False if not in database or outdated
    return True if in database and up to date
    Note: this don't update the database"""
    try:
        data = Summoner_tb.select().where(
            Summoner_tb.name == summoner.name
        ).get()
        if str(data.revisionDate) == str(summoner.revision_date):
            return True
        else:
            return False
    except Exception:
        return False

def store_summoner(summoner: Summoner):
    """store summoner in DB or if it's already there update it if outdated"""
    try:
        Summoner_tb.create(
            region = summoner.region,
            name = summoner.name,
            profile_icon_id = summoner.profile_icon_id,
            revisionDate = summoner.revision_date,
            level = summoner.level,
            mastery_score = summoner.mastery_score
        )
    except IntegrityError:
        summoner_row = Summoner_tb.get(name=summoner.name)
        if str(summoner_row.revisionDate) != str(summoner.revision_date):
            summoner_row.profile_icon_id = summoner.profile_icon_id,
            summoner_row.revisionDate = summoner.revision_date,
            summoner_row.level = summoner.level,
            summoner_row.mastery_score = summoner.mastery_score
            summoner_row.save()


try:
    player = Summoner('player')
    print(player.level)
    print(player.mastery_score)
    store_summoner(player)
except SummonerNameInvalid:
    pass
except SummonerNotFound:
    pass
except OverRateLimit:
    pass
except HTTPError:
    pass
