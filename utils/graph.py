"""
This file contains functions that can be used throughout the project.
"""

from neo4j import GraphDatabase, basic_auth
from neo4j.spatial import WGS84Point
import pandas as pd


class Graph:
    
    def __init__(self, uri, username, password):
        self.uri = uri
        self.username = username
        self.password = password
        self.driver = self.create_driver()

    def create_driver(self):
        driver = GraphDatabase.driver(
            self.uri, auth=basic_auth(self.username, self.password)
        )
            self.uri, auth=basic_auth(self.username, self.password)
        )
        return driver

    def read_query(self, cypher_query, parameters):
    def read_query(self, cypher_query, parameters):
        with self.driver.session(database="neo4j") as session:
            results = session.execute_read(
                lambda tx: tx.run(cypher_query, parameters).data()
            )
        self.driver.close()

        return results


    def query_run(self, query, parameters):
        """This is the function used to run queries.

        Args:
            query (String): Cypher query to run
            parameters (Dict): dictionary of parameters

        Returns:
            results: query run output
        """
        with self.driver.session(database="neo4j") as session:
            results = session.run(query, parameters).data()
            results = session.run(query, parameters).data()
        self.driver.close()

        print(results)

    def query_run_df(self, query, parameters):
        with self.driver.session(database="neo4j") as session:
            result = session.run(query, parameters)
            result = session.run(query, parameters)
            df = pd.DataFrame([r.values() for r in result], columns=result.keys())
        self.driver.close()

        return df

    def create_competitors(self):
        company_query = """
        company_query = """
            LOAD CSV WITH HEADERS FROM "file://" AS line
            MERGE (a:Company {id: line.source_id, name: line.source_name})
            MERGE (b:Company {id: line.target_id, name: line.targte_name})
            MERGE (a)-[:COMPETES]-(b)
            RETURN a,b
            """
            """

        results = self.query_run(company_query, {})

        print(results)

    def create_constraints(self):
        company_constraint_query = """
        CREATE CONSTRAINT company_id FOR (a:Company) REQUIRE a.id IS UNIQUE;
        """

        competitor_constraint_query = """
        CREATE CONSTRAINT competitor_id FOR ()<-[comp:COMPETES]->() REQUIRE comp.id IS NOT NULL;
        """
        parent_constraint_query = """
        """
        parent_constraint_query = """
        CREATE CONSTRAINT parent_id FOR ()-[comp:ULTIMATE_PARENT_OF]->() REQUIRE comp.id IS NOT NULL;
        """
        partner_constraint_query = """
        """
        partner_constraint_query = """
        CREATE CONSTRAINT partner_id FOR ()<-[comp:PARTNERS]->() REQUIRE comp.id IS NOT NULL;
        """
        supplier_constraint_query = """
        """
        supplier_constraint_query = """
        CREATE CONSTRAINT supplier_id FOR ()-[comp:SUPPLIES]->() REQUIRE comp.id IS NOT NULL;
        """

        self.query_run(company_constraint_query, {})
        self.query_run(competitor_constraint_query, {})
        self.query_run(parent_constraint_query, {})
        self.query_run(partner_constraint_query, {})
        self.query_run(supplier_constraint_query, {})


    def create_company(self):
        company_query = """
        company_query = """
        LOAD CSV WITH HEADERS FROM 'file:///companies.csv' AS line
        MERGE (a:Company {id: line.id, name: line.name})
        RETURN a
        """
        """
        print(self.query_run(company_query, {}))

    def create_sector(self):
        nace_query = """
        LOAD CSV WITH HEADERS FROM 'file:///info.csv' AS line
        MERGE (s:Sector {sector: line.sector})
        MERGE (i:Industry {industry: line.industry})
        MERGE (i)-[:IN_SECTOR]->(s)
        RETURN s,i
        """

        print(self.query_run(nace_query, {}))

    def add_sector_info(self):
        sector_query = """
        sector_query = """
        LOAD CSV WITH HEADERS FROM 'file:///info.csv' AS line
        MATCH (i:Industry {industry: line.industry})
        MATCH (a:Company {id: line.id})
        MERGE (a)-[:IN_INDUSTRY]->(i)
        ON CREATE 
            SET 
                a.code = line.code,
                a.nace_description = line.nace_description
        RETURN a,i
        """
        print(self.query_run(sector_query, {}))

    def add_location_info(self):
        loc_query = """
        LOAD CSV WITH HEADERS FROM 'file:///addresses.csv' AS line
        MATCH (a:Company {id: line.id})
        SET a.country = line.country
        SET a.city_state_postal = line.city_state_postal
        SET a.location_street1 = line.location_street1
        SET a.point = point({latitude:toFloat(line.lat), longitude:toFloat(line.log)})
        RETURN a
        """
        print(self.query_run(loc_query, {}))

    def create_competitors(self):
        competitors_query = """
        competitors_query = """
        LOAD CSV WITH HEADERS FROM 'file:///competitors.csv' AS line
        MATCH (a:Company {id: line.source_id})
        MATCH (b:Company {id: line.target_id})
        MERGE (a)-[:COMPETES {id: line.index, date: line.start_date}]-(b)
        RETURN a,b
        """
        """

        print(self.query_run(competitors_query, {}))

    def create_parents(self):
        competitors_query = """
        competitors_query = """
        LOAD CSV WITH HEADERS FROM 'file:///parents.csv' AS line
        MATCH (a:Company {id: line.source_id})
        SET a:Ultimate_Parent
        WITH a,line
        MATCH (b:Company {id: line.target_id})
        MERGE (a)-[:ULTIMATE_PARENT_OF {id: line.index, date: line.start_date}]->(b)
        RETURN a,b
        """

        """

        print(self.query_run(competitors_query, {}))

    def create_partners(self):
        competitors_query = """
        competitors_query = """
        LOAD CSV WITH HEADERS FROM 'file:///partners.csv' AS line
        MATCH (a:Company {id: line.source_id})
        MATCH (b:Company {id: line.target_id})
        MERGE (a)-[:PARTNERS {id: line.index, date: line.start_date}]-(b)
        RETURN a,b
        """
        """

        print(self.query_run(competitors_query, {}))

    def create_suppliers(self):
        competitors_query = """
        competitors_query = """
        LOAD CSV WITH HEADERS FROM 'file:///suppliers.csv' AS line
        MATCH (a:Company {id: line.source_id})
        SET a:Supplier
        WITH a,line
        MATCH (b:Company {id: line.target_id})
        MERGE (a)-[:SUPPLIES {id: line.index, date: line.start_date, revenue_pct:line.revenue_pct}]->(b)
        RETURN a,b
        """
        """

        print(self.query_run(competitors_query, {}))

    def clear_database(self):
        clear_query = """
        clear_query = """
        MATCH (n) DETACH DELETE n;
        """
        """

        print(self.query_run(clear_query, {}))


    def drop_constraints(self):
        company_constraint_query = """
        DROP CONSTRAINT company_id;
        """

        competitor_constraint_query = """
        DROP CONSTRAINT competitor_id;
        """
        parent_constraint_query = """
        """
        parent_constraint_query = """
        DROP CONSTRAINT parent_id;
        """
        partner_constraint_query = """
        """
        partner_constraint_query = """
        DROP CONSTRAINT partner_id;
        """
        supplier_constraint_query = """
        """
        supplier_constraint_query = """
        DROP CONSTRAINT supplier_id;
        """

        self.query_run(company_constraint_query, {})
        self.query_run(competitor_constraint_query, {})
        self.query_run(parent_constraint_query, {})
        self.query_run(partner_constraint_query, {})
        self.query_run(supplier_constraint_query, {})


# import pandas as pd
# first = Graph('bolt://44.198.170.36:7687', 'neo4j', 'procurements-compensation-decibel')

# competitors = pd.read_parquet('data/competitors.parquet.gzip')
# print(first.create_person(competitors))
