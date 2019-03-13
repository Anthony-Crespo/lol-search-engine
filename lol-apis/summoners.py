from peewee import (SqliteDatabase, Model, CharField, IntegerField,
                    IntegrityError)

db = SqliteDatabase('summoners.db')

class Summoner(Model):
    region = CharField(max_length=5)
    name = CharField(max_length=32, unique=True)
    profile_icon_id = IntegerField()
    revisionDate = CharField(default=0)
    level = IntegerField(default=0)
    mastery_score = IntegerField(default=0)

    class Meta:
        database = db
        legacy_table_names=False
        # unique name by region
        indexes = (
        (('region', 'name'), True),
        )
    

if __name__ == '__main__':
    db.connect()
    db.create_tables([Summoner], safe=True)
