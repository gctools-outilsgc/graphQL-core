import graphene
import GCprofile.schema


class Query(GCprofile.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
