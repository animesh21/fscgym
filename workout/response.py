from rest_framework.response import Response


class StandardResponse(Response):
    def __init__(self, status, message, data, *args, **kwargs):
        super().__init__(
            data={'status': status, 'message': message, 'data': data}, status=status, *args, **kwargs
        )
