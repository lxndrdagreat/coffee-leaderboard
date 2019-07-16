from tortoise.models import Model
from tortoise import fields


class UserProfile(Model):
    username = fields.CharField(max_length=255, unique=True)
    experience = fields.IntField(default=0)
    level = fields.IntField(default=1)
    prestige = fields.IntField(default=0)
    private = fields.BooleanField(default=True)


class CoffeeEntry(Model):
    # user = fields.CharField(max_length=255)
    user = fields.ForeignKeyField('models.UserProfile', on_delete=fields.CASCADE)
    text = fields.CharField(max_length=500)
    channel_id = fields.CharField(max_length=255)
    channel_name = fields.CharField(max_length=255)
    date = fields.BigIntField()


class UserAppToken(Model):
    user = fields.ForeignKeyField('models.UserProfile', on_delete=fields.CASCADE)
    # this is the token that the user copies/pastes
    auth_token = fields.CharField(max_length=200, unique=True)

    # this is the token that the app actually makes requests with
    app_token = fields.CharField(max_length=200, unique=True, null=True)
