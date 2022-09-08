from marshmallow import Schema, fields, INCLUDE

class studioSchema(Schema):
    id = fields.Integer()
    name = fields.Str()

class producerSchema(Schema):
    id = fields.Integer()
    name = fields.Str()

class moviesSchema(Schema):
    id = fields.Integer()
    title = fields.Str()
    release = fields.Integer()
    winner = fields.Boolean()
    class Meta:
        unknown = INCLUDE

class movieProducerSchema(Schema):
    id = fields.Integer()
    idmovie = fields.Integer()
    idproducer = fields.Integer()

class movieStudioSchema(Schema):
    id = fields.Integer()
    idmovie = fields.Integer()
    idstudio = fields.Integer()