from rest_framework.pagination import PageNumberPagination

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000
    def get_paginated_response(self, *args, **kwargs):
        response = super(LargeResultsSetPagination, self).get_paginated_response(*args, **kwargs)
        response.data['total_pages'] = self.page.paginator.num_pages
        return response

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000
    def get_paginated_response(self, *args, **kwargs):
        response = super(StandardResultsSetPagination, self).get_paginated_response(*args, **kwargs)
        response.data['total_pages'] = self.page.paginator.num_pages
        return response

class SmallResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    def get_paginated_response(self, *args, **kwargs):
        response = super(SmallResultsSetPagination, self).get_paginated_response(*args, **kwargs)
        response.data['total_pages'] = self.page.paginator.num_pages
        return response
