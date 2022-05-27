from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from re import compile

EXEMPT_URLS = [compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [compile(url) for url in settings.LOGIN_EXEMPT_URLS]


class protectRoute:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_view(self, request, view_func, *view_args, **view_kargs):
        assert hasattr(request, 'user')
        if not request.user.is_authenticated:
            path = request.path_info.lstrip('/')
            if not any(m.match(path) for m in EXEMPT_URLS):
                return redirect(settings.LOGIN_URL)
        else:  # if user authenticated prevent to not access login route again
            path = request.path_info.lstrip('/')
            if any(m.match(path) for m in EXEMPT_URLS):
                return redirect('manage_store:dashboard')
