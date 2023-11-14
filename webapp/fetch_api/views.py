from rest_framework.views import APIView
from rest_framework.response import Response

from .utils import (
    count_nodes,
    fetch_nodes,
    fetch_node_details,
    fetch_countries,
    fetch_industries,
    # fetch_data_source,
    fetch_continents,
)


class GetNodesCount(APIView):
    def get(self, request):
        count_info = {
            'node_type': request.GET.get('t', 'Company'),
            'name': request.GET.get('q', ''),
            'country': request.GET.get('c', ''),
            'jurisdiction': request.GET.get('j', ''),
        }
        count = count_nodes(count_info)
        data = {
            'response': {
                'status': '200',
                'data': count,
            },
        }
        return Response(data)


class GetNodesData(APIView):
    def get(self, request):
        fetch_info = {
            'node_type': request.GET.get('t', 'Company'),
            'name': request.GET.get('q', ''),
            'country': request.GET.get('c', ''),
            'jurisdiction': request.GET.get('j', ''),
            'limit': 10,
            'page': int(request.GET.get('p', 1)),
        }
        nodes = fetch_nodes(fetch_info)
        data = {
            'response': {
                'status': '200',
                'rows': len(nodes),
                'data': nodes,
            },
        }
        return Response(data)


class GetNodeData(APIView):
    def get(self, request):
        node_info = {
            'node_type': request.GET.get('t', 'Company'),
            'node_id': int(request.GET.get('id')),
        }
        node_details = fetch_node_details(node_info)
        data = {
            'response': {
                'status': '200',
                'data': node_details,
            },
        }
        return Response(data)


class GetCountries(APIView):
    def get(self, request):
        countries = fetch_countries()
        data = {
            'response': {
                'status': '200',
                'data': countries,
            },
        }
        return Response(data)


class GetIndustries(APIView):
    def get(self, request):
        industries = fetch_industries()
        data = {
            'response': {
                'status': '200',
                'data': industries,
            },
        }
        return Response(data)

class GetContinents(APIView):
    def get(self, request):
        continents = fetch_continents()
        data = {
            'response': {
                'status': '200',
                'data': continents,
            },
        }
        return Response(data)

# class GetDataSource(APIView):
#     def get(self, request):
#         data_source = fetch_data_source()
#         data = {
#             'response': {
#                 'status': '200',
#                 'data': data_source,
#             },
#         }
#         return Response(data)
