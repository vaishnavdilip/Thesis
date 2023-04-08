MATCH (movie:Movie {title:"The Matrix"})<-[:ACTED_IN]-(actor)-[:ACTED_IN]->(rec:Movie)
RETURN distinct rec.title as title LIMIT 20