from django.template import loader
from django.http import HttpResponse
import redis


def index(request):
    data = redis_data()
    context = {'data': data}
    template = loader.get_template('web/redis_data.html')
    return HttpResponse(template.render(context, request))


def redis_data():
    data = {}
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    keys = r.keys('*')
    for key in keys:
        skey = key.decode("utf-8")
        ktype = r.type(key)
        if ktype == b'string':
            data[skey] = str(r.get(key).decode("utf-8"))
        if ktype == b'hash':
            data[skey] = str(r.hgetall(key))
        if ktype == b'list':
            data[skey] = r.lrange(key, 0, -1)
    return data
