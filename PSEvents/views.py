from django.http import HttpResponse
from django.views import View


# Create your views here.
class EventView(View):
    def get(self, request):
        return HttpResponse('hi for the first time')