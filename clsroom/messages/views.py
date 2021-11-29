import json
from rest_framework.views import APIView


class MessageView(APIView):
    
    def post (self, request):
        data : dict = json.loads(request.body)
        
