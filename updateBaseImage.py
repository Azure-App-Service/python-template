import requests
import argparse
import json
import time
import threading
import sys


def getConfig(config):
    f = open(config, "r")
    content = json.loads(f.read(), strict=False)
    f.close()
    return content


def writeConfig(content, file):
    f = open(file, "w+")
    f.write(json.dumps(content, indent=4, sort_keys=True))
    f.close()

parser = argparse.ArgumentParser()
parser.add_argument('--newOryxTimestamp', "-t", help='new oryx timestamp EG: 20190628.2', required=True)
args = parser.parse_args()

newOryxTimestamp = args.newOryxTimestamp

configs = ["blessedImageConfig-dev.json", 
    "blessedImageConfig-master.json", 
    "blessedImageConfig-save.json", 
    "blessedImageConfig-temp.json"]

for config in configs:
    buildRequests = getConfig(config)
    for br in buildRequests:
        newBaseImageName = "mcr.microsoft.com/oryx/" + br["stack"] + ":" + br["version"] + "-" + newOryxTimestamp
        br.update( { "baseImageName": newBaseImageName })
    writeConfig(buildRequests, config)
