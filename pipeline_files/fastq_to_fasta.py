"""
Simple script to parse a consensus fastq files and convert to fasta files
suitable for BOLD manual submission
Author: Jackson Eyres
Copyright: Government of Canada
License: MIT
"""

import argparse
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import glob
import os

def main():
    parser = argparse.ArgumentParser(description='Parses Fastq Files')
    parser.add_argument('-d', type=str,
                        help='Directory of consensus fastqs', required=True)
    parser.add_argument('-o', type=str,
                        help='Output File', required=True)
    args = parser.parse_args()

    parse_fastq(args.d, args.o)


def parse_fastq(directory, output):
    """
    Takes a fastq generated by consensus and extracts fasta sequence with basic quality metric
    Quality is deteremined by counting the presence of Ns, uncapitilized letters and degenerate bases
    :param directory:
    :return:
    """
    fastqs = glob.glob(os.path.join(directory, "*.fq"))
    records = []
    for fastq in fastqs:
        with open(fastq) as f:
            basename = os.path.basename(fastq).replace(".fq", "")
            for seq in SeqIO.parse(f,"fastq"):

                length = len(seq.seq)
                good_bases = str(seq.seq).count("A") + \
                              str(seq.seq).count("C") + \
                              str(seq.seq).count("T") + \
                              str(seq.seq).count("G")
                rough_quality = length - good_bases
                record = SeqRecord(Seq(str(seq.seq)), id=basename,
                                   description="Low Quality Positions: {}".format(rough_quality))
                records.append(record)


    # Writes fasta files to sequence

    with open(output, "w") as g:
        for record in records:
            SeqIO.write(record, g, "fasta")


if __name__ == "__main__":
    main()