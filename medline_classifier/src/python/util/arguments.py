import argparse
import json


print 'parsing arguments'

_argparser = argparse.ArgumentParser(description="Plot the error rate "
                                        "distribution.")
_argparser.add_argument(
    "-c",
    help="Path to the config file",
    required=False,
    default="../../config/config.json"
)
_argparser.add_argument(
    "--in",
    help="Path to the input file",
    required=False
)
_argparser.add_argument(
    "--out",
    help="Path to the output file",
    required=False
)
_argparser.add_argument(
    "--years",
    help="Path to the output file",
    required=False
)
_argparser.add_argument(
    "--only-major",
    help="Indicates whether non-major topics should be ignored",
    action='store_true'
)
_args = _argparser.parse_args()

settings = None

with open(_args.c) as f:
    print 'loading config file: ' + _args.c
    settings = json.load(f)

    # override with values from the arguments
    for key in vars(_args):
        value = getattr(_args, key)
        settings[key] = value
        print key + ': ' + str(value)
