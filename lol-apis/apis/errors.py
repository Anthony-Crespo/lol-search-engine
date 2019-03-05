class SummonerNotFound(Exception):
    """Raise when summoner is not found"""

class SummonerNameInvalid(Exception):
    """Summoner name is not valid"""

class OverRateLimit(Exception):
    "Rate limit exceeded"

# error name name an update
class ApiKeyError(Exception):
    """API key is wrong or expired or endpoint got removed"""

def notOk(response):
    """Raise custom error for most frequent errors
    and show default requests.exceptions.HTTPError message for others.
    Remember that each region use a different server.

    Args:
        response (Response): Response from requests 
    Raises:
        SummonerNotFound: response status_code 404
        NameError: response status_code 429
        ApiKeyError: response status_code 403
        HTTPError: response status_code not 200:

        """
    if response.status_code == 200:
        return False
    elif response.status_code == 404:
        raise SummonerNotFound(
            "Summoner was not found and may not exist (error 404)")
    elif response.status_code == 429:
        raise OverRateLimit("The rate limit was exceeded (error 424)")
    elif response.status_code == 403:
        raise ApiKeyError(
            "Riot API key may be wrong or expired" 
            " and/or endpoints need an update (error 403)"
        )
    else:
        response.raise_for_status()
