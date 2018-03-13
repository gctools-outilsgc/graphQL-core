import graphene
import profile.schema


class Query(profile.schema.ProfileQuery, graphene.ObjectType):
    pass


class Mutation(profile.schema.ProfileMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
