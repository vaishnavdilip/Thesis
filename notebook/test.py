import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

from utils import Graph

cypher_query = '''
MATCH (movie:Movie {title:"The Matrix"})<-[:ACTED_IN]-(actor)-[:ACTED_IN]->(rec:Movie)
 RETURN distinct rec.title as title LIMIT 20
'''

first = Graph("bolt://44.204.52.109:7687", "neo4j","card-twirls-workbook")
print(first.write_query(cypher_query))