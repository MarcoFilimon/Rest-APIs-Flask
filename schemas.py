# Data validation

from marshmallow import Schema, fields


# To avoid infinite nesting, we are renaming our schemas which don't use nested fields to Plain, such as PlainItemSchema and PlainStoreSchema.

# Then the schemas that do use nesting can be called ItemSchema and StoreSchema, and they inherit from the plain schemas. This reduces duplication and prevents infinite nesting.

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

# This code is used to add extra fields to the item schema.
# Particularly, fields.Nested means that it will add the fields corresponding to the PlainStoreSchema.
# dumply_only means that it will only add these fields when we dump (return) the schema in a POST request for example. (python object to JSON)
class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class StoreSchema(PlainStoreSchema):
    # List() because a store can have multiple items.
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