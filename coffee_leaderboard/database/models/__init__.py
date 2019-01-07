from tortoise.models import Model
from tortoise import fields


class CoffeeEntry(Model):
    user = fields.CharField(max_length=255)
    text = fields.CharField(max_length=500)
    channel_id = fields.CharField(max_length=255)
    channel_name = fields.CharField(max_length=255)
    date = fields.BigIntField()
