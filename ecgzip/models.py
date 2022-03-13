from django.db import models


class CompressedECG(models.Model):
    id = models.UUIDField(primary_key=True)
    original_size = models.IntegerField()
    data = models.FileField()

    @property
    def size(self):
        return self.data.size

    @property
    def compression_ratio(self):
        return self.original_size / self.size
