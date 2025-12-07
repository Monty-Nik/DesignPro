from rest_framework import mixins
from rest_framework import generics
from .models import Snippet
from .serializers import SnippetSerializer


from .models import Snippet
from .serializers import SnippetSerializer


class SnippetList(generics.ListCreateAPIView):
   queryset = Snippet.objects.all()
   serializer_class = SnippetSerializer


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
   queryset = Snippet.objects.all()
   serializer_class = SnippetSerializer

   def get(self, request, *args, **kwargs):
       return self.retrieve(request, *args, **kwargs)

   def put(self, request, *args, **kwargs):
       return self.update(request, *args, **kwargs)

   def delete(self, request, *args, **kwargs):
       return self.destroy(request, *args, **kwargs)
