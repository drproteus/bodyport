from django.shortcuts import redirect, render, HttpResponse
from django.http import Http404
from django.urls import reverse
from django.views import View
from ecgzip.forms import CompressionForm
from ecgzip.models import CompressedECG
from uuid import uuid4


class ECGCompress(View):
    def get(self, request):
        return render(request, "ecgzip/compress.html", {})

    def post(self, request):
        form = CompressionForm(request.POST, request.FILES)
        if not form.is_valid():
            return HttpResponse(form.errors, status=500)
        record = form.save()
        return redirect(
            reverse("compression-result", kwargs={"compression_id": record.id})
        )


class ECGCompressionResult(View):
    def get(self, request, compression_id):
        try:
            record = CompressedECG.objects.get(id=compression_id)
        except CompressedECG.DoesNotExist:
            raise Http404
        return render(
            request,
            "ecgzip/result.html",
            {
                "size": record.size,
                "original_size": record.original_size,
                "compression_ratio": record.compression_ratio,
                "link": record.data.url,
            },
        )
