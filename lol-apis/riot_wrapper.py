from apis import RiotApi
from apis import SummonerNameInvalid, SummonerNotFound, OverRateLimit
from summoners import IntegrityError, DoesNotExist, Summoner
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


def summoner_db(summoner_name, region = riot_api.default_region):
    """Return the summoner row
    
    Request data to api 
    if up to date in DB return row and stop requesting data from apis
    else update before returning
    if summoner missing from DB create row before returning it

    Note: riot_api.default_region is used here because get_summoner update it
    on call. (region can have typos but not riot_api.default_region)
    """
    summoner = riot_api.get_summoner(summoner_name, region)
    try:
        summoner_row = Summoner.get(name=summoner['name'], region=riot_api.default_region)
        if summoner['revisionDate'] == summoner_row.revisionDate:
            pass
        else:
            summoner_row.profile_icon_id = summoner['profileIconId']
            summoner_row.revisionDate = summoner['revisionDate']
            summoner_row.level = summoner['summonerLevel']
            summoner_row.mastery_score = riot_api.get_total_mastery(summoner['id'])
            summoner_row.save()
        return summoner_row
    except DoesNotExist:
        try:
            Summoner.create(
                accountId = summoner['accountId'],
                region = riot_api.default_region,
                name = summoner['name'],
                profile_icon_id = summoner['profileIconId'],
                revisionDate = summoner['revisionDate'],
                level = summoner['summonerLevel'],
                mastery_score = riot_api.get_total_mastery(summoner['id'])
            )
            return Summoner.get(name=summoner['name'], region=riot_api.default_region)
        except IntegrityError:
            pass


def summoner_data_in_db(summoner_name: str, summoner_region: str):
    """Check if a summoner is in the database and up to date
    return False if not in database or outdated
    return True if in database and up to date
    Note: this don't update the database"""
    summoner = riot_api.get_summoner(summoner_name, summoner_region)
    try:
        data = Summoner.select().where(
            Summoner.name == summoner['name'],
            Summoner.region == riot_api.default_region
        ).get()
        if data.revisionDate == summoner['revisionDate']:
            return True
        else:
            return False
    except Exception:
        return False


try:
    player = summoner_db('player')
    print(player.level)
    print(player.mastery_score)
except SummonerNameInvalid:
    pass
except SummonerNotFound:
    pass
except OverRateLimit:
    pass
except HTTPError:
    pass
