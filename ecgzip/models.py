from django.db import models


class CompressedECG(models.Model):
    id = models.UUIDField(primary_key=True)
    original_size = models.IntegerField()
    data = models.FileField(upload_to="compressed")
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def size(self):
        return self.data.size

    @property
    def compression_ratio(self):
        return self.original_size / self.size


class DecompressedECG(models.Model):
    id = models.UUIDField(primary_key=True)
    data = models.FileField(upload_to="decompressed")
    created_at = models.DateTimeField(auto_now_add=True)
