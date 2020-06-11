from datetime import datetime, timedelta
from django.contrib.auth.backends import ModelBackend
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

    def authenticate(self, request=None, **kwargs):
        username = None
        try:
            username = kwargs[self.username_key]
        except KeyError:
            if not self.no_username:
                raise

        if request is not None:
            counts = self.get_counters(request)
            print(counts)
            if sum(counts.values()) >= self.requests:
                print('Limit reached..')
                raise

        else:
            print('No request')

        user = ModelBackend.authenticate(self,
                                         request=request, **kwargs
                                         )
        if user is None and request is not None:
            print('Login Failed')
            cache_key = self.get_cache_key(request)
            self.cache_incr(cache_key)
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
