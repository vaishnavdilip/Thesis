from neomodel import db

countries = db.cypher_query(
    '''
    MATCH (n:Country)
    RETURN DISTINCT n.country AS countries
    '''
)[0]

industries = db.cypher_query(
    '''
    MATCH (n:Industry)
    RETURN DISTINCT n.name AS industries
    '''
)[0]

continents = db.cypher_query(
    '''
    MATCH (n:Continent)
    RETURN DISTINCT n.continent AS continents
    '''
)[0]

COUNTRIES = sorted([country[0] for country in countries])
INDUSTRIES = sorted([industry[0] for industry in industries])
CONTINENTS = sorted([continent[0] for continent in continents])
