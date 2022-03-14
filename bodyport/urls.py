from django.contrib import admin
from django.urls import path
from ecgzip.views import (
    ECGCompress,
    ECGCompressionResult,
    ECGDecompress,
    ECGDecompressionResult,
)

urlpatterns = [
    path("", ECGCompress.as_view(), name="ecg-compress"),
    path(
        "result/<uuid:compression_id>/",
        ECGCompressionResult.as_view(),
        name="compression-result",
    ),
    path("decompress/", ECGDecompress.as_view(), name="ecg-decompress"),
    path(
        "original/<uuid:decompression_id>/",
        ECGDecompressionResult.as_view(),
        name="decompression-result",
    ),
]
