from util.compression import ECGCompressor


def test_decompression_restores_from_compression():
    with open("test/data/sample_ecg_raw.bin", "rb") as f:
        original = f.read()
    compressed = ECGCompressor.compress(original)
    decompressed = ECGCompressor.decompress(compressed)
    assert original == decompressed
