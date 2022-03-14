from django import forms
from django.core.files.base import ContentFile
from uuid import uuid4
from ecgzip.models import CompressedECG, DecompressedECG
from util.compression import ECGCompressor


class CompressionForm(forms.Form):
    data = forms.FileField()

    def save(self):
        data = self.cleaned_data["data"].read()
        compressed = ECGCompressor.compress(data)
        record_id = uuid4()
        record = CompressedECG.objects.create(
            id=record_id,
            original_size=len(data),
            data=ContentFile(compressed, name=f"{record_id}.ecgz"),
        )
        return record


class DecompressionForm(forms.Form):
    data = forms.FileField()

    def save(self):
        data = self.cleaned_data["data"].read()
        original = ECGCompressor.decompress(data)
        record_id = uuid4()
        record = DecompressedECG.objects.create(
            id=record_id,
            data=ContentFile(original, name=f"{record_id}.bin")
        )
        return record
