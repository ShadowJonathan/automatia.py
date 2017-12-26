# SimpleQuery
# ComplexQuery
# StringQuery
# BoolQuery
# HasNextArg
# TODO WRITE THIS

import automatia



def BoolQuery(query="", default=False):
    for q in query.split("\n"):
        automatia.Inform(q)
