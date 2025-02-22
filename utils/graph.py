"""
This file contains functions that can be used throughout the project.
"""

from neo4j import GraphDatabase, basic_auth, AsyncGraphDatabase
from neo4j.spatial import WGS84Point
import pandas as pd
import asyncio


class Graph:
    def __init__(self, uri, username, password):
        self.uri = uri
        self.username = username
        self.password = password
        self.driver = self.create_driver()
        self.async_driver = self.create_async_driver()

    def create_driver(self):
        driver = GraphDatabase.driver(
            self.uri, auth=basic_auth(self.username, self.password)
        )
        return driver

    async def create_async_driver(self):
        driver = AsyncGraphDatabase.driver(
            self.uri, auth=basic_auth(self.username, self.password)
        )
        return driver

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
        self.driver.close()

        print(results)

    def query_run_df(self, query, parameters):
        with self.driver.session(database="neo4j") as session:
            result = session.run(query, parameters)
            df = pd.DataFrame([r.values() for r in result], columns=result.keys())
        self.driver.close()

        return df

    async def query_run_async(self, query, parameters):
        async with AsyncGraphDatabase.driver(
            self.uri, auth=(self.username, self.password)
        ) as driver:
            async with driver.session(database="neo4j") as session:
                records = await session.run(query, parameters)
                df = pd.DataFrame(await records.values(), columns=records.keys())
                return df

    def create_competitors(self):
        company_query = """
            LOAD CSV WITH HEADERS FROM "file://" AS line
            MERGE (a:Company {id: line.source_id, name: line.source_name})
            MERGE (b:Company {id: line.target_id, name: line.targte_name})
            MERGE (a)-[:COMPETES]-(b)
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
        CREATE CONSTRAINT parent_id FOR ()-[comp:ULTIMATE_PARENT_OF]->() REQUIRE comp.id IS NOT NULL;
        """
        partner_constraint_query = """
        CREATE CONSTRAINT partner_id FOR ()<-[comp:PARTNERS]->() REQUIRE comp.id IS NOT NULL;
        """

        supplier_constraint_query = """
        CREATE CONSTRAINT supplier_id FOR ()-[comp:SUPPLIES_TO]->() REQUIRE comp.id IS NOT NULL;
        """

        self.query_run(company_constraint_query, {})
        self.query_run(competitor_constraint_query, {})
        self.query_run(parent_constraint_query, {})
        self.query_run(partner_constraint_query, {})
        self.query_run(supplier_constraint_query, {})

    def create_company(self):
        company_query = """
        LOAD CSV WITH HEADERS FROM 'file:///companies.csv' AS line
        MERGE (:Company {id: line.id, name: line.name})
        """
        print(self.query_run(company_query, {}))

    def create_sector(self):
        nace_query = """
        LOAD CSV WITH HEADERS FROM 'file:///info.csv' AS line
        MERGE (n:Nace {code: line.code, description: line.nace_description})
        MERGE (s:Sector {name: line.sector})
        MERGE (i:Industry {name: line.industry})
        MERGE (n)-[:IN_INDUSTRY]->(i)-[:IN_SECTOR]->(s)
        """

        print(self.query_run(nace_query, {}))

    def add_sector_info(self):
        sector_query = """
        LOAD CSV WITH HEADERS FROM 'file:///info.csv' AS line
        MATCH (i:Nace {code: line.code})
        MATCH (a:Company {id: line.id})
        MERGE (a)-[:IN_CATEGORY]->(i)
        ON CREATE 
            SET 
                a.industries = line.industry,
                a.sector = line.sector
        """
        print(self.query_run(sector_query, {}))

    def create_locations(self):
        locations_query = """ 
        LOAD CSV WITH HEADERS FROM 'file:///addresses.csv' AS line
        MERGE (s:Continent {continent: line.Continent})
        MERGE (i:Country {country: line.country})
        MERGE (i)-[:IN_CONTINENT]->(s)
        """
        print(self.query_run(locations_query, {}))

    def add_location_info(self):
        loc_query = """
        LOAD CSV WITH HEADERS FROM 'file:///addresses.csv' AS line

        MATCH (i:Country {country: line.country})
        MATCH (a:Company {id: line.id})
        MERGE (a)-[:IN_COUNTRY]->(i)
        ON CREATE 
            SET 
                a.city_state_postal = line.city_state_postal,
                a.location_street1 = line.location_street1,
                a.point = point({latitude:toFloat(line.lat), longitude:toFloat(line.log)}),
                a.countries = line.country,
                a.country_code = line.countrycode
        """
        print(self.query_run(loc_query, {}))

    def create_competitors(self):
        competitors_query = """
        LOAD CSV WITH HEADERS FROM 'file:///competitors.csv' AS line
        MATCH (a:Company {id: line.source_id})
        MATCH (b:Company {id: line.target_id})
        MERGE (a)<-[:COMPETES {id: line.index, date: line.start_date}]->(b)
        """

        print(self.query_run(competitors_query, {}))

    def create_parents(self):
        competitors_query = """
        LOAD CSV WITH HEADERS FROM 'file:///parents.csv' AS line
        MATCH (a:Company {id: line.source_id})
        MATCH (b:Company {id: line.target_id})
        MERGE (a)-[:ULTIMATE_PARENT_OF {id: line.index, date: line.start_date}]->(b)
        """

        print(self.query_run(competitors_query, {}))

    def create_partners(self):
        competitors_query = """
        LOAD CSV WITH HEADERS FROM 'file:///partners.csv' AS line
        MATCH (a:Company {id: line.source_id})
        MATCH (b:Company {id: line.target_id})
        MERGE (a)<-[:PARTNERS {id: line.index, date: line.start_date}]->(b)
        """

        print(self.query_run(competitors_query, {}))

    def create_suppliers(self):
        competitors_query = """
        LOAD CSV WITH HEADERS FROM 'file:///suppliers.csv' AS line
        MATCH (a:Company {id: line.source_id})
        MATCH (b:Company {id: line.target_id})
        MERGE (a)-[r:SUPPLIES_TO]->(b)
        ON CREATE
            SET
                r.id = line.index, 
                r.date = line.start_date, 
                r.revenue_pct = line.revenue_pct,
                r.distance = point.distance(a.point, b.point)     
        """

        print(self.query_run(competitors_query, {}))

    def clear_database(self):
        clear_query = """
        MATCH (n) DETACH DELETE n;
        """

        print(self.query_run(clear_query, {}))

    def drop_constraints(self):
        company_constraint_query = """
        DROP CONSTRAINT company_id IF EXISTS;
        """

        competitor_constraint_query = """
        DROP CONSTRAINT competitor_id IF EXISTS;
        """

        parent_constraint_query = """
        DROP CONSTRAINT parent_id IF EXISTS;
        """

        partner_constraint_query = """
        DROP CONSTRAINT partner_id IF EXISTS;
        """

        supplier_constraint_query = """
        DROP CONSTRAINT supplier_id IF EXISTS;
        """

        new_constraint_query = """
        DROP CONSTRAINT constraint_unique_Company_pk IF EXISTS;
        """

        self.query_run(company_constraint_query, {})
        self.query_run(competitor_constraint_query, {})
        self.query_run(parent_constraint_query, {})
        self.query_run(partner_constraint_query, {})
        self.query_run(supplier_constraint_query, {})
        self.query_run(new_constraint_query, {})

    def add_index(self):
        index_query = """
        CREATE FULLTEXT INDEX companyName FOR (n:Company) ON EACH [n.name];
        """

        self.query_run(index_query, {})


# import pandas as pd
# first = Graph('bolt://44.198.170.36:7687', 'neo4j', 'procurements-compensation-decibel')

# competitors = pd.read_parquet('data/competitors.parquet.gzip')
# print(first.create_person(competitors))
