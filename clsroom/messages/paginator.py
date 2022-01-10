# from rest_framework.pagination import CursorPagination, PageNumberPagination
# from rest_framework.response import Response


# class CommentPaginator(CursorPagination):
#     page = 1
#     page_size = 5
#     cursor_query_param = 'page_size'
#     ordering = '-created_at'


#     # def get_paginated_response(self, data):
#     #     next_link = self.get_next_link()
#     #     if next_link is not None:
#     #         next_link = next_link[next_link.index('?'):len(next_link)]
#     #     return Response({
#     #         'links' : {
#     #             'next' : next_link,
#     #             'previous' : self.get_next_link()
#     #         },
#     #         'comments' : data,
#     #     })

#     def generate_response(self, query_set, serializer_obj, request):
#         try:
#             page_data = self.paginate_queryset(query_set, request)
#         except:
#             return Response({"error": "No results found for the requested page"}, status=status.HTTP_400_BAD_REQUEST)

#         serialized_page = serializer_obj(page_data, many=True)
#         return self.get_paginated_response(serialized_page.data)