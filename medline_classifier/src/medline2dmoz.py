import argparse
import os

from parsers.medline_json import MedlineFileParser


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description="Generate data with constant error rate")
    argparser.add_argument("-d", help="MEDLINE input directory", type=str)

    args = argparser.parse_args()

    dir_name = args.d

    paths = os.listdir(dir_name)
    files = [os.path.join(path) for path in paths if os.path.isfile(os.path.join(dir_name, path))]

    for file in files:
        parser = MedlineFileParser(file)
        parser.parse()
        # TODO for testing only parse one file
        break
