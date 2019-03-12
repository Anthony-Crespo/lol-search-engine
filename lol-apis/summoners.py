from peewee import (SqliteDatabase, Model, CharField, IntegerField, 
                    IntegrityError)

db = SqliteDatabase('summoners.db')

class Summoner(Model):
    name = CharField(max_length=32, unique=True)
    level = IntegerField(default=0)
    revisionDate = CharField(default=0)

    class Meta:
        database = db
        legacy_table_names=False


def summoner_data(summoner_name: str, revisionDate: int = '0'):
    """Check if a summoner is in the database and updated
    return False if not in database
    return Summoner object if data is up to date else update before return"""
    try:
        data = Summoner.select().where(Summoner.name == summoner_name).get()
    except Exception:
        return False
    
    if revisionDate == data.revisionDate:
        return data
    else:
        pass  # request apis and update database before returning it
