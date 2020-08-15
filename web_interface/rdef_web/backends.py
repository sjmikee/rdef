from datetime import datetime, timedelta
#from django.contrib.auth import authenticate as realauth
import django.contrib.auth
from django.core.cache import cache


class RateLimitMixin(object):
    """
    A mixin to enable rate-limiting in an existing authentication backend.
    """
    cache_prefix = 'ratelimitbackend-'
    minutes = 1
    requests = 3
    username_key = 'username'
    no_username = False

    def limited_authenticate(self, request=None, username=None, password=None):
        if request is not None:
            counts = self.get_counters(request)
            print(counts)
            if not counts:
                pass
            elif sum(counts.values()) >= self.requests:
                print('Limit reached..')
                raise

        else:
            print('No request')

        # user = ModelBackend.authenticate(self,
        #                                 request=request, **kwargs
        #                                 )
        print(username)
        print(password)
        try:
            user = self.authenticate(
                username=username, password=password)
        except Exception as e:
            print(e)
        if user is None and request is not None:
            print('Login Failed')
            cache_key = self.get_cache_key(request)
            self.cache_incr(cache_key)
        print(user)
        return user

    def get_counters(self, request):
        return cache.get_many(self.keys_to_check(request))

    def keys_to_check(self, request):
        now = datetime.now()
        return [
            self.key(
                request,
                now - timedelta(minutes=minute),
            ) for minute in range(self.minutes + 1)
        ]

    def get_cache_key(self, request):
        return self.key(request, datetime.now())

    def key(self, request, dt):
        return '%s%s-%s' % (
            self.cache_prefix,
            self.get_ip(request),
            dt.strftime('%Y%m%d%H%M'),
        )

    def get_ip(self, request):
        return request.META['REMOTE_ADDR']

    def cache_incr(self, key):
        """
        Non-atomic cache increment operation. Not optimal but
        consistent across different cache backends.
        """
        cache.set(key, cache.get(key, 0) + 1, self.expire_after())

    def expire_after(self):
        """Cache expiry delay"""
        return (self.minutes + 1) * 60
