from django.contrib import admin
from django.urls import path
from ecgzip.views import ECGCompress, ECGCompressionResult

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", ECGCompress.as_view(), name="ecg-compress"),
    path(
        "result/<uuid:compression_id>/",
        ECGCompressionResult.as_view(),
        name="compression-result",
    ),
]
