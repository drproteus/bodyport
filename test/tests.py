from util.compression import ECGCompressor
from util.formats import ECGData, ECGCompressed


def test_decompression_restores_from_compression():
    with open("test/data/sample_ecg_raw.bin", "rb") as f:
        original = f.read()
    compressed = ECGCompressor.compress(original)
    decompressed = ECGCompressor.decompress(compressed)
    assert original == decompressed


def test_compression_structure():
    test_sequence = [0, 1000, 340, 65534, 4570]
    deltas = [0, 1000, 340, 65534, 4570]
    small = [0, 1000, -660]
    big = [65194, -60964]
    locs = [3, 4]
    test_data = ECGCompressed.parse(
        ECGCompressor.compress(ECGData.build(test_sequence))
    )
    assert test_data["len_origin"] == len(deltas)
    assert test_data["len_small"] == len(small)
    assert test_data["len_big"] == len(big)
    assert test_data["len_locs"] == len(locs)
    assert test_data["small"] == small
    assert test_data["big"] == big
    assert test_data["locs"] == locs
