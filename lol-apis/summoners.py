from peewee import (SqliteDatabase, Model, CharField, IntegerField,
                    IntegrityError, DoesNotExist)

db = SqliteDatabase('summoners.db')

# The accountId isn't unique by key, but is it unique by dev acount?
class Summoner(Model):
    accountId = CharField()
    region = CharField(max_length=5)
    name = CharField(max_length=32)
    profile_icon_id = IntegerField()
    # next can be none if summoner created with match data
    revisionDate = IntegerField(null = True)
    level = IntegerField(null = True)
    mastery_score = IntegerField(null = True)

    class Meta:
        database = db
        legacy_table_names=False
        # unique name by region
        indexes = (
        (('region', 'name'), True),
        )

    # Add **kwargs for not required fields
    @classmethod
    def create_summoner(cls, accountId, region, name, profile_icon_id):
        try:
            with db.transaction():
                cls.create(
                    accountId = accountId,
                    region = region,
                    name = name,
                    profile_icon_id = profile_icon_id)
        except IntegrityError:
            raise ValueError("Summoner already exists")

def initialize():
    """Create the database and the table if they don't exist."""
    db.connect()
    db.create_tables([Summoner], safe=True)
    db.close()
    

if __name__ == '__main__':
    initialize()
