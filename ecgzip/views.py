from django.shortcuts import redirect, render, HttpResponse
from django.http import Http404
from django.urls import reverse
from django.views import View
from ecgzip.forms import CompressionForm, DecompressionForm
from ecgzip.models import CompressedECG, DecompressedECG
from uuid import uuid4


class ECGCompress(View):
    def get(self, request):
        return render(request, "ecgzip/compress.html", {})

    def post(self, request):
        form = CompressionForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(
                request, "ecgzip/compress.html", {"errors": form.errors.as_ul()}
            )
        try:
            record = form.save()
        except Exception as e:
            return render(
                request, "ecgzip/compress.html", {"errors": e}
            )
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


class ECGDecompress(View):
    def get(self, request):
        return render(request, "ecgzip/decompress.html", {})

    def post(self, request):
        form = DecompressionForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(
                request, "ecgzip/decompress.html", {"errors": form.errors.as_ul()}
            )
        try:
            record = form.save()
        except Exception as e:
            return render(
                request, "ecgzip/decompress.html", {"errors": e}
            )
        return redirect(
            reverse("decompression-result", kwargs={"decompression_id": record.id})
        )


class ECGDecompressionResult(View):
    def get(self, request, decompression_id):
        try:
            record = DecompressedECG.objects.get(id=decompression_id)
        except DecompressedECG.DoesNotExist:
            raise Http404
        return render(
            request, "ecgzip/original.html", {"link": record.data.url}
        )
