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
_args = _argparser.parse_args()

settings = None

with open(_args.c) as f:
    print 'loading config file: ' + _args.c
    settings = json.load(f)
