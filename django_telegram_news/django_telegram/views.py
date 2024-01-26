from rest_framework.views import APIView
from rest_framework.response import Response
import json

class NewsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            with open('./django_telegram/data.json', 'r') as file:
                data = json.load(file)
            return Response(data)
        except FileNotFoundError:
            return Response({"error": "Data not found"}, status=404)
from django.shortcuts import render

def news_view(request):
    return render(request, 'news.html')
