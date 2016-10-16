from django.template import loader
from django.http import HttpResponse
import redis
from django.conf import settings
import collections


def data(request):
    req_obj = request.GET.copy()
    env = req_obj.get("db")
    r_data = redis_data(env)
    context = {'data': r_data, 'env': env.upper()}
    template = loader.get_template('web/redis_data.html')
    return HttpResponse(template.render(context, request))


def redis_data(endpoint):
    r_data = collections.OrderedDict()
    redis_config = settings.REDIS_CONFIG
    if endpoint == 'prod':
        redis_object = redis.StrictRedis(host=redis_config.get('host'), port=redis_config.get('port'),
                                         db=redis_config.get('db'))
    else:
        redis_object = redis.StrictRedis(host='localhost', port=6379, db=0)
    keys = redis_object.keys('*')
    format_data(keys, r_data, redis_object)
    return r_data


def format_data(keys, r_data, redis_object):
    for key in keys:
        s_key = key.decode("utf-8")
        k_type = redis_object.type(key)
        if k_type == b'string':
            m = redis_object.get(key).decode("utf-8")
            if m in ['healthy', 'unhealthy']:
                r_data[s_key] = m
        # elif k_type == b'hash':
        #     r_data[s_key] = redis_object.hgetall(key)
        # elif k_type == b'list':
        #     r_data[s_key] = redis_object.lrange(key, 0, -1)
