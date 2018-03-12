import graphene
import profile.schema


class Query(profile.schema.Query, graphene.ObjectType):
    pass


class Mutation(profile.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
