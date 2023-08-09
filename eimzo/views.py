import os
from django.conf import settings
from django.http import (HttpRequest, 
                        HttpResponse, 
                        HttpResponseForbidden, 
                        HttpResponseNotFound,
                        HttpResponseBadRequest)

from .models import Key

def download_certificate(request: HttpRequest, filename:str) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    try:
        if not filename.endswith(".pfx"):
            return HttpResponseBadRequest()
        
        key = Key.objects.get(file=filename)
        file_path = os.path.join(settings.BASE_DIR, "uploads", filename)
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                response = HttpResponse(f.read(), content_type="application/x_pkcs12")
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                return response
        else:
            return HttpResponseNotFound("File not found")
    except Key.DoesNotExist:
        return HttpResponseNotFound()
        

