from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.core.files.base import ContentFile
from util.compression import ECGCompressor
from ecgzip.forms import CompressionForm
from ecgzip.models import CompressedECG
from uuid import uuid4

from django.views.decorators.csrf import csrf_exempt # DEBUG!!!


@csrf_exempt
def ecg_compress(request):
    form = CompressionForm(request.POST, request.FILES)
    print(request.POST)
    if not form.is_valid():
        print(form.errors)
        return HttpResponse(status=500)
    record = form.save()
    return JsonResponse(
        {
            "size": record.size,
            "original_size": record.original_size,
            "compression_ratio": record.compression_ratio,
            "link": record.data.url,
        }
    )
