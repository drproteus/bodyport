from django.test import TestCase, Client
from ecgzip.models import CompressedECG, DecompressedECG
from util.compression import ECGCompressor
from util.formats import ECGData, ECGCompressed


class CompressionPageTestCase(TestCase):
    def test_can_upload_and_compress(self):
        c = Client()
        with open("test/data/sample_ecg_raw.bin", "rb") as f:
            c.post("", {"data": f})
        assert CompressedECG.objects.count() == 1

    def test_verify_compressed_upload(self):
        c = Client()
        with open("test/data/sample_ecg_raw.bin", "rb") as f:
            c.post("", {"data": f})
        with open("test/data/sample_ecg_raw.bin", "rb") as f:
            expected = ECGCompressor.compress(f.read())
        actual = CompressedECG.objects.first().data.read()
        assert expected == actual


class DecompressionPageTestCase(TestCase):
    def test_can_upload_and_decompress(self):
        c = Client()
        with open("test/data/sample_ecg_compressed.ecgz", "rb") as f:
            c.post("/decompress/", {"data": f})
        assert DecompressedECG.objects.count() == 1

    def test_verify_decompressed_upload(self):
        c = Client()
        with open("test/data/sample_ecg_compressed.ecgz", "rb") as f:
            c.post("/decompress/", {"data": f})
        with open("test/data/sample_ecg_compressed.ecgz", "rb") as f:
            expected = ECGCompressor.decompress(f.read())
        actual = DecompressedECG.objects.first().data.read()
        assert expected == actual
