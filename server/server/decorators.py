from django.http import HttpResponseRedirect
import settings


def anonymous_required(view_function, redirect_to=None):
    """ Function to check if user is not authenticated
    """

    return AnonymousRequired(view_function, redirect_to)


class AnonymousRequired(object):
    """ Class for the above function. Does the work.
    """

    def __init__(self, view_function, redirect_to):
        if redirect_to is None:
            from django.conf import settings
            redirect_to = settings.LOGIN_REDIRECT_URL
        self.view_function = view_function
        self.redirect_to = redirect_to

    def __call__(self, request, *args, **kwargs):
        if request.user is not None and request.user.is_authenticated():
            return HttpResponseRedirect(self.redirect_to)
        if not settings.LOGIN_REQUIRED and self.view_function.__name__ == 'login':
            return HttpResponseRedirect('/')
        return self.view_function(request, *args, **kwargs)


def check_login(view_function, redirect_to=settings.LOGIN_URL):
    """ Custom decorator to check if login is required, then force users to authenticate
    """

    return CheckLogin(view_function, redirect_to)


class CheckLogin(object):
    """ Does the magic for the above function
    """

    def __init__(self, view_function, redirect_to):
        if redirect_to is None:
            from django.conf import settings
            redirect_to = settings.LOGIN_REDIRECT_URL
        self.view_function = view_function
        self.redirect_to = redirect_to

    def __call__(self, request, *args, **kwargs):
        if settings.LOGIN_REQUIRED:
            if not request.user.is_authenticated():
                return HttpResponseRedirect(self.redirect_to)
        if not settings.LOGIN_REQUIRED and self.view_function.__name__ == 'logout':
            return HttpResponseRedirect('/')
        return self.view_function(request, *args, **kwargs)