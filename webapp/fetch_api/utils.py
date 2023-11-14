from .constants import COUNTRIES, INDUSTRIES, CONTINENTS

from .models import (
    Company,
    Continent,
    Country,
    Industry,
    Sector,
)

# For easily access each of the model classes programmatically, create a key-value map.
MODEL_ENTITIES = {
    'Company' : Company,
    'Continent' : Continent,
    'Country' : Country,
    'Industry' : Industry,
    'Sector' : Sector,
}


###################################################################
# Queries Functions
###################################################################

def filter_nodes(node_type, search_text, country, industry):
    node_set = node_type.nodes

    # On Address nodes we want to check the search_text against the address property
    # For any other we check against the name property
    if node_type.__name__ == 'Country':
        node_set.filter(country__icontains=search_text)
    elif node_type.__name__ == 'Continent':
        node_set.filter(continent__icontains=search_text)
    else:
        node_set.filter(name__icontains=search_text)

    # Only entities store jurisdiction info
    # if node_type.__name__ == 'Sector':
    #     node_set.filter(name__icontains=search_text)
    
    # if node_type.__name__ == 'Industry':
    #     node_set.filter(name__icontains=search_text)

    if node_type.__name__ == 'Company':
        node_set.filter(countries__icontains=country)
        print(len(node_set))
        node_set.filter(industries__icontains=industry)
        print(len(node_set))

    # node_set.filter(sourceID__icontains=source_id)

    return node_set


def count_nodes(count_info):
    count = {}
    node_type               = count_info['node_type']
    search_word             = count_info['name']
    country                 = count_info['country']
    jurisdiction            = count_info['jurisdiction']
    node_set                = filter_nodes(MODEL_ENTITIES[node_type], search_word, country, jurisdiction)

    count['count']          = len(node_set)

    return count


def fetch_nodes(fetch_info):
    node_type       = fetch_info['node_type']
    search_word     = fetch_info['name']
    country         = fetch_info['country']
    limit           = fetch_info['limit']
    start           = ((fetch_info['page'] - 1) * limit)
    end             = start + limit
    jurisdiction    = fetch_info['jurisdiction']
    node_set        = filter_nodes(MODEL_ENTITIES[node_type], search_word, country, jurisdiction)

    fetched_nodes   = node_set[start:end]

    return [node.serialize for node in fetched_nodes]


def fetch_node_details(node_info):
    node_type       = node_info['node_type']
    node_id         = node_info['node_id']
    node            = MODEL_ENTITIES[node_type].nodes.get(id=node_id)
    node_details    = node.serialize

    # Make sure to return an empty array if not connections
    node_details['node_connections'] = []
    if (hasattr(node, 'serialize_connections')):
        node_details['node_connections'] = node.serialize_connections

    return node_details


def fetch_countries():
    return COUNTRIES


def fetch_industries():
    return INDUSTRIES

def fetch_continents():
    return CONTINENTS

def fetch_data_source():
    return 'https://offshoreleaks.icij.org/pages/database'
