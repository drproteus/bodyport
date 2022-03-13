from util.formats import ECGData, ECGCompressed


class ECGCompressor:
    MAX = 32767
    MIN = -32767

    @classmethod
    def delta_encode(cls, data):
        last = 0
        buffer = []
        for i in range(len(data)):
            current = data[i]
            buffer.append(current - last)
            last = current
        return buffer

    @classmethod
    def delta_decode(cls, data):
        last = 0
        buffer = []
        for i in range(len(data)):
            delta = data[i]
            buffer.append(delta + last)
            last = buffer[i]
        return buffer

    @classmethod
    def find_big_values(cls, data):
        locations = []
        for i, d in enumerate(data):
            if d > cls.MAX or d < cls.MIN:
                locations.append(i)
        return locations

    @classmethod
    def compress(cls, ecg_bytes):
        data = ECGData.parse(ecg_bytes)
        deltas = cls.delta_encode(data)
        locs = cls.find_big_values(deltas)
        small = [d for d in deltas if d <= cls.MAX and d >= cls.MIN]
        big = [d for d in deltas if d > cls.MAX or d < cls.MIN]
        return ECGCompressed.build(
            {
                "len_origin": len(data),
                "len_small": len(small),
                "len_big": len(big),
                "len_locs": len(locs),
                "small": small,
                "big": big,
                "locs": locs,
            }
        )

    @classmethod
    def decompress(cls, comp_bytes):
        data = ECGCompressed.parse(comp_bytes)
        deltas = []
        big_i = 0
        small_i = 0
        for i in range(data["len_origin"]):
            if big_i < len(data["locs"]) and i == data["locs"][big_i]:
                deltas.append(data["big"][big_i])
                big_i += 1
            else:
                deltas.append(data["small"][small_i])
                small_i += 1
        original = cls.delta_decode(deltas)
        return ECGData.build(original)
