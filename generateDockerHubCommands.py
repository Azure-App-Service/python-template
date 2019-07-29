import requests
import argparse
import json
import time
import threading
import sys
import datetime


def getConfig(config):
    f = open(config, "r")
    content = json.loads(f.read(), strict=False)
    f.close()
    return content

parser = argparse.ArgumentParser()
parser.add_argument('--newTag', "-t", help='new timestamp EG: 1906281234')
args = parser.parse_args()

if args.newTag == None:
    tag = datetime.datetime.now().strftime("%y%m%d%H%M")
else:
    tag = args.newTag

config = "blessedImageConfig-dev.json"

buildRequests = getConfig(config)
print("az login")
print("az acr login --name blimpacr")
for br in buildRequests:
    print("docker pull blimpacr.azurecr.io/{}".format(br["outputImageName"]))
    print("docker tag blimpacr.azurecr.io/{} appsvctest/{}:{}_{}".format(br["outputImageName"], br["stack"], br["version"], tag))
    print("docker tag blimpacr.azurecr.io/{} appsvc/{}:{}_{}".format(br["outputImageName"], br["stack"], br["version"], tag))
    print("docker push appsvctest/{}:{}_{}".format(br["stack"], br["version"], tag))
    print("docker push appsvc/{}:{}_{}".format(br["stack"], br["version"], tag))

    ### LATEST / LTS ###
    if br["version"] == "3.7":
        print("docker pull blimpacr.azurecr.io/{}".format(br["outputImageName"]))
        print("docker tag blimpacr.azurecr.io/{} appsvctest/{}:{}_{}".format(br["outputImageName"], br["stack"], "latest", tag))
        print("docker tag blimpacr.azurecr.io/{} appsvctest/{}:{}".format(br["outputImageName"], br["stack"], "latest"))
        print("docker tag blimpacr.azurecr.io/{} appsvc/{}:{}_{}".format(br["outputImageName"], br["stack"], "latest", tag))
        print("docker tag blimpacr.azurecr.io/{} appsvc/{}:{}".format(br["outputImageName"], br["stack"], "latest"))
        print("docker push appsvctest/{}:{}_{}".format(br["stack"], "latest", tag))
        print("docker push appsvctest/{}:{}".format(br["stack"], "latest"))
        print("docker push appsvc/{}:{}_{}".format(br["stack"], "latest", tag))
        print("docker push appsvc/{}:{}".format(br["stack"], "latest"))
