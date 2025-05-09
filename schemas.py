# Data validation

from marshmallow import Schema, fields

class PlainItemSchema(Schema):
	id = fields.Int(dump_only=True)  # only used to be returning data to the client (field is read-only)
	name = fields.Str(required=True)
	price = fields.Float(required=True)

class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()

class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)

class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema())
    tag = fields.Nested(TagSchema())

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=lambda x: len(x) > 0)
    password = fields.Str(required=True, load_only=True)  # load_only means that the field is only used for input (not returned to the client)
    # this load_only can be visualized  when you run "GET" command. if it's present in the response, it means that it's not load_only.
    # this is a good practice to not expose the password to the client.