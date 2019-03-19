from peewee import (SqliteDatabase, Model, CharField, IntegerField,
                    IntegrityError, DoesNotExist)

db = SqliteDatabase('summoners.db')

# The accountId isn't unique by key, but is it unique by dev acount?
class Summoner(Model):
    accountId = CharField()
    region = CharField(max_length=5)
    name = CharField(max_length=32)
    profile_icon_id = IntegerField()
    revisionDate = IntegerField()
    level = IntegerField(default=0)
    mastery_score = IntegerField(default=0)

    class Meta:
        database = db
        legacy_table_names=False
        # unique name by region
        indexes = (
        (('region', 'name'), True),
        )

def initialize():
    """Create the database and the table if they don't exist."""
    db.connect()
    db.create_tables([Summoner], safe=True)
    

if __name__ == '__main__':
    initialize()
