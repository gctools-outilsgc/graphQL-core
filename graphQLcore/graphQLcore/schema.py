import graphene
import GCprofile.schema


class Query(GCprofile.schema.Query, graphene.ObjectType):
    pass


class Mutation(GCprofile.schema.CreateProfileData, GCprofile.schema.ModifyProfileData, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
