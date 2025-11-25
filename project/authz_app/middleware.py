from django.http import HttpResponseForbidden

class AccessControlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Проверка доступности ресурса для текущего пользователя
        access_conditions = getattr(view_func, 'required_access', {})

        if access_conditions:
            # Получаем значение атрибута "required_access", где указаны обязательные условия доступа
            # Например: {'role': 'Администратор'}
            role = access_conditions.get('role')

            if role and not request.user.has_role(role):
                return HttpResponseForbidden("Доступ запрещён.")

        return None