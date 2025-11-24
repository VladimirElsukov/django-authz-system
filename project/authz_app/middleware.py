from django.http import HttpResponseForbidden


class AccessControlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Проверяем доступность ресурса для текущего пользователя
        required_role = getattr(view_func, 'required_role', None)

        if required_role and not request.user.has_role(required_role):
            return HttpResponseForbidden("Доступ запрещён.")
        return None