import os
import json

Config = {}

def parseConfig(configFilePath=None):

    if configFilePath:
        with open(configFilePath) as configFile:
            return json.load(configFile)

    return {}


def parsePipelineConfig():
    global Config
    
    configFilePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

    Config = parseConfig(configFilePath)

parsePipelineConfig()