from django.http import JsonResponse
from django.middleware.csrf import CsrfViewMiddleware

class JsonCsrfMiddleware(CsrfViewMiddleware):
    def _reject(self, request, reason):
        return JsonResponse({"error": "CSRF Failed", "reason": reason}, status=403)
