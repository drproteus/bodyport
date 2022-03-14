import click
from util.compression import ECGCompressor


@click.command()
@click.option("-d", "--decompress", default=False, is_flag=True)
@click.option("-c", "--compress", default=False, is_flag=True)
@click.argument("infile", type=click.Path(exists=True))
@click.argument("outfile")
def ecgzip(decompress, compress, infile, outfile):
    if not (decompress or compress) or (decompress and compress):
        raise click.BadParameter(
            "One of compression or decompression must be specified."
        )
    with open(infile, "rb") as f:
        indata = f.read()
    if compress:
        outdata = ECGCompressor.compress(indata)
    elif decompress:
        outdata = ECGCompressor.decompress(indata)
    with open(outfile, "wb") as f:
        f.write(outdata)


if __name__ == "__main__":
    ecgzip()
