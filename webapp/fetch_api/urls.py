from django.urls import re_path

from .views import (
    GetNodesCount,
    GetNodesData,
    GetNodeData,
    GetCountries,
    GetIndustries,
    GetContinents,
    # GetDataSource,
)


urlpatterns = [
    re_path(r'^count[/]?$', GetNodesCount.as_view(), name='get_nodes_count'),
    re_path(r'^nodes[/]?$', GetNodesData.as_view(), name='get_nodes_data'),
    re_path(r'^node[/]?$', GetNodeData.as_view(), name='get_node_data'),
    re_path(r'^countries[/]?$', GetCountries.as_view(), name='get_countries'),
    re_path(r'^industries[/]?$', GetIndustries.as_view(), name='get_industries'),
    re_path(r'^continents[/]?$', GetContinents.as_view(), name='get_continents'),
    # re_path(r'^datasource[/]?$', GetDataSource.as_view(), name='get_data_source'),
]
