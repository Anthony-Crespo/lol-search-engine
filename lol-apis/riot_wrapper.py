from apis import RiotApi
from apis import SummonerNameInvalid, SummonerNotFound, OverRateLimit
from summoners import IntegrityError, DoesNotExist, Summoner
from matches import Match
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
        if summoner['revisionDate'] != summoner_row.revisionDate:
            summoner_row.profile_icon_id = summoner['profileIconId']
            summoner_row.level = summoner['summonerLevel']
            summoner_row.mastery_score = riot_api.get_total_mastery(summoner['id'])
            summoner_row.save()
        data = summoner_row
    except DoesNotExist:
        Summoner.create(
            accountId = summoner['accountId'],
            region = riot_api.default_region,
            name = summoner['name'],
            profile_icon_id = summoner['profileIconId'],
            level = summoner['summonerLevel'],
            mastery_score = riot_api.get_total_mastery(summoner['id'])
        )
        data = Summoner.get(name=summoner['name'], region=riot_api.default_region)

    try:
        matchlist = riot_api.get_match_history(summoner['accountId'], beginTime=data.revisionDate)['matches']
    except SummonerNotFound:
        matchlist = []
    # if this goes 404 is cause there is no new match!
    for match in matchlist:
        query = Match.select().where(Match.gameId == match['gameId'])
        if not query.exists():
            Match.create(
                platformId = match['platformId'],
                gameId = match['gameId'],
                champion = match['champion'],
                queue = match['queue'],
                season = match['season'],
                timestamp = match['timestamp'],
                role = match['role'],
                lane = match['lane']
            )
    
    # update revisionDate at the very end to prevent missing matches when bug
    data.revisionDate = summoner['revisionDate']
    data.save()
    return data


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
    from summoners import initialize as initialize_summoners
    from matches import initialize as initialize_matches
    initialize_summoners()
    initialize_matches()

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
