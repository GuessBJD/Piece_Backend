import random
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_next_page_number(self):
        if not self.page.has_next():
            return None
        return self.page.next_page_number()

    def get_previous_page_number(self):
        if not self.page.has_previous():
            return None
        return self.page.previous_page_number()

    def get_paginated_response(self, data):
        
        return Response({
            'page': {
                'loaded_pages': self.page.number,
                'next_page': self.get_next_page_number(),
                'last_page': self.page.paginator.num_pages,
            },
            'count': self.page.paginator.count,
            'results': data
        })
    
class RandomResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10

    def get_page_number(self, request, paginator):
        page_number = request.query_params.get(self.page_query_param) or (random.randint(1, paginator.num_pages) if paginator.num_pages > 1 else 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages
        return page_number
    
    def get_paginated_response(self, data):
        
        return Response({
            'count': self.page.paginator.count,
            'results': data
        })