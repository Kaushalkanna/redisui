from django.template import loader
from django.http import HttpResponse


def index(request):
    context = {'hello': 'hello'}
    template = loader.get_template('web/redis_data.html')
    return HttpResponse(template.render(context, request))