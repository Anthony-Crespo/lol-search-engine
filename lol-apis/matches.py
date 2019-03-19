from peewee import (SqliteDatabase, Model, CharField, IntegerField, TextField
                    )

db = SqliteDatabase('matches.db')

class Match(Model):
    # each match create with this first block of data
    # data is in player matchlist
    platformId = CharField()
    gameId = IntegerField(unique=True)
    champion = IntegerField()
    queue = IntegerField()
    season = IntegerField()
    timestamp = IntegerField()
    role = CharField()
    lane = CharField()

    # this is only accesible when searched by gameid
    # add only if needed
    # this may need: default = None
    gameCreation = IntegerField(null = True)
    gameDuration = IntegerField(null = True)
    queueId = IntegerField(null = True)
    mapId = IntegerField(null = True)
    seasonId = IntegerField(null = True)
    gameVersion = CharField(null = True)
    gameMode = CharField(null = True)
    gameType = CharField(null = True)
    teams = TextField(null = True)
    participants = TextField(null = True)
    participantIdentities = TextField(null = True)

    class Meta:
        database = db
        legacy_table_names=False

def initialize():
    """Create the database and the table if they don't exist."""
    db.connect()
    db.create_tables([Match], safe=True)
    

if __name__ == '__main__':
    initialize()
