import re

# ^[0-9\\p{L} _\\.]+$ (riot example)
# ATM: it only accept words char, periods, underscore and space
# double check summoner name naming rules
def summoner_name_valid(summoner_name: str):
    """Validate a summoner name with official naming rules from Riot
    
    Args:
        summoner_name (str): the string to validate
    Returns: 
        Return False if special characters found in name else return True
    Raises:
        SummonerNotFound: response status_code 404
        NameError: response status_code 429
        ApiKeyError: response status_code 403
        HTTPError: response status_code not 200:
        
    """
    pattern = re.compile(r'[^\w\.\s]')
    matches = pattern.search(summoner_name)
    return True if matches is None else False
