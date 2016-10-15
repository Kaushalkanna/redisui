from django.template import loader
from django.http import HttpResponse
import redis
from django.conf import settings
import collections


def index(request):
    data = redis_data()
    context = {'data': data}
    template = loader.get_template('web/redis_data.html')
    return HttpResponse(template.render(context, request))


def redis_data():
    data = collections.OrderedDict()
    redis_config = settings.REDIS_CONFIG
    redis_object = redis.StrictRedis(host=redis_config.get('host', ''), port=redis_config.get('port'),
                                     db=redis_config.get('db'))
    keys = redis_object.keys('*')
    for key in keys:
        skey = key.decode("utf-8")
        ktype = redis_object.type(key)
        if ktype == b'string':
            data[skey] = redis_object.get(key).decode("utf-8")
        elif ktype == b'hash':
            data[skey] = redis_object.hgetall(key)
        elif ktype == b'list':
            data[skey] = redis_object.lrange(key, 0, -1)
    return data
