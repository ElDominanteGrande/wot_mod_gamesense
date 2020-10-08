import json
import requests
import os
import time
from enum import Enum
from config import Config as cfg

import mod_gamesense_logger as logger


class Mode(Enum):
    COUNT           = "count"
    PERCENT         = "percent"
    COLOR           = "color"
    CONTEXTCOLOR    = "context-color"


class JsonBase():
    def getJson(self):
        return json.dumps(self.getPyData())

    def getPyData(self):
        return {}


class StaticColor(JsonBase):

    minColorValue = 0
    maxColorValue = 255

    def __init__(self, red, green, blue):
        # super(StaticColor, self).__init__()

        self.red = max(min(red, self.maxColorValue), self.minColorValue)
        self.green = max(min(green, self.maxColorValue), self.minColorValue)
        self.blue = max(min(blue, self.maxColorValue), self.minColorValue)

    # override
    def getPyData(self):
        return {"red": self.red, "green":self.green, "blue":self.blue}


class GradientColor(JsonBase):
    def __init__(self, zero, hundred):
        # super(GradientColor, self).__init__()

        self.zero = zero
        self.hundred = hundred

    # override
    def getPyData(self):
        return {"gradient" : {"zero": self.zero.getPyData(), "hundred":self.hundred.getPyData()}}


class RangeColorBase(JsonBase):
    def __init__(self):
        # super(RangeFrequencyBase, self).__init__()
        pass


class RangeColor(RangeColorBase):
    def __init__(self, low, high, color):
        # super(RangeColor, self).__init__()

        self.low = low
        self.high = high
        self.color = color

    # override
    def getPyData(self):
        if isinstance(self.color,(list, tuple)) and all(isinstance(elem,(RangeColorBase, StaticColor, GradientColor)) for elem in self.color):
            colorPyData = [x.getPyData() for x in self.color]
        else:
            colorPyData = self.color.getPyData()

        return {"low": self.low, "high":self.high, "color":colorPyData}


class RangeFrequencyBase(JsonBase):
    def __init__(self):
        # super(RangeFrequencyBase, self).__init__()
        pass


class RangeFrequency(RangeFrequencyBase):
    def __init__(self, low, high, frequency):
        # super(RangeFrequency, self).__init__()

        self.low = low
        self.high = high
        self.frequency = frequency

    # override
    def getPyData(self):
        if isinstance(self.frequency,(list, tuple)) and all(isinstance(elem,RangeFrequencyBase) for elem in self.frequency):
            frequencyPyData = [x.getPyData() for x in self.frequency]
        else:
            frequencyPyData = self.frequency

        return {"low": self.low, "high":self.high, "frequency":frequencyPyData}


class RangeRepeatLimitBase(JsonBase):
    def __init__(self):
        # super(RangeRepeatLimitBase, self).__init__()
        pass


class RangeRepeatLimit(RangeRepeatLimitBase):
    def __init__(self, low, high, repeat_limit):
        # super(RangeRepeatLimit, self).__init__()

        self.low = low
        self.high = high
        self.repeat_limit = repeat_limit

    # override
    def getPyData(self):
        if isinstance(self.repeat_limit,(list, tuple)) and all(isinstance(elem,RangeRepeatLimitBase) for elem in self.repeat_limit):
            repeat_limitPyData = [x.getPyData() for x in self.repeat_limit]
        else:
            repeat_limitPyData = self.repeat_limit

        return {"low": self.low, "high":self.high, "repeat_limit":repeat_limitPyData}


class Rate(JsonBase):
    def __init__(self, frequency, repeat_limit):
        # super(Rate, self).__init__()

        self.frequency = frequency
        self.repeat_limit = repeat_limit

    # override
    def getPyData(self):
        
        if isinstance(self.frequency,(list, tuple)) and all(isinstance(elem,RangeFrequency) for elem in self.frequency):
            frequencyPyData = [x.getPyData() for x in self.frequency]
        else:
            frequencyPyData = self.frequency

        if self.repeat_limit:
            if isinstance(self.repeat_limit,(list, tuple)) and all(isinstance(elem,RangeRepeatLimit) for elem in self.repeat_limit):
                repeat_limitPyData = [x.getPyData() for x in self.repeat_limit]
            else:
                repeat_limitPyData = self.repeat_limit

            return {"frequency": frequencyPyData, "repeat_limit":repeat_limitPyData}
        else:
            return {"frequency": frequencyPyData}


class ColorHandler(JsonBase):
    def __init__(self, devicetype, zone, mode, color, rate=None, contextframekey=None):
        # super(ColorHandler, self).__init__()

        self.devicetype = devicetype
        self.zone = zone
        self.mode = mode
        self.color = color
        self.rate = rate
        self.contextframekey = contextframekey

    # override
    def getPyData(self):
        if not self.contextframekey and self.color:
            if isinstance(self.color, (list, tuple)) and all(isinstance(elem, RangeColor) for elem in self.color):
                colorPyData = [x.getPyData() for x in self.color]
            else:
                colorPyData = self.color.getPyData()

            if isinstance(self.zone, str):
                if not self.rate:
                    return {"device-type":self.devicetype, "zone":self.zone, "mode":self.mode.value, "color":colorPyData}
                else:
                    return {"device-type":self.devicetype, "zone":self.zone, "mode":self.mode.value, "color":colorPyData, "rate":self.rate.getPyData()}
            elif isinstance(self.zone, dict):
                if not self.rate:
                    return {"device-type":self.devicetype, "custom-zone-keys":self.zone["custom-zone-keys"], "mode":self.mode.value, "color":colorPyData}
                else:
                    return {"device-type":self.devicetype, "custom-zone-keys":self.zone["custom-zone-keys"], "mode":self.mode.value, "color":colorPyData, "rate":self.rate.getPyData()}

        elif self.mode.value == Mode.CONTEXTCOLOR:
            if isinstance(self.zone, str):
                return {"device-type":self.devicetype, "zone":self.zone, "mode":self.mode.value, "context-frame-key":self.contextframekey}
            elif isinstance(self.zone, dict):
                return {"device-type":self.devicetype, "custom-zone-keys":self.zone["custom-zone-keys"], "mode":self.mode.value, "context-frame-key":self.contextframekey}


class GameEventBinder(JsonBase):
    def __init__(self, game, event, min_value, max_value, icon_id, handlers):
        # super(GameEventBinder, self).__init__()

        self.game = game
        self.event = event
        self.min_value = min_value
        self.max_value = max_value
        self.icon_id = icon_id
        self.handlers = handlers

    # override
    def getPyData(self):
        handlerJsonString = []
        for handler in self.handlers:
            handlerJsonString.append(handler.getPyData())

        return {"game":self.game, "event":self.event, "min_value":self.min_value, "max_value":self.max_value, "icon_id":self.icon_id, "handlers":handlerJsonString}


def getAccessInformation():
    urlPrefix = "http://"
    dataHeader = {'Content-type': 'application/json'}
    parsedPortInfo = readSteelseriesEnginePort()

    return (urlPrefix, dataHeader, parsedPortInfo)


def bindGameEvent(game, event, min_value, max_value, icon_id, devicetype, zone, mode, handlers):

    urlPrefix, dataHeader, parsedPortInfo = getAccessInformation()
    urlSteelseriesEngineBind = urlPrefix + parsedPortInfo["address"] + "/bind_game_event"

    myEventBinder = GameEventBinder(game, event, min_value, max_value, icon_id, handlers)

    response = requests.post(urlSteelseriesEngineBind, data = myEventBinder.getJson(), headers = dataHeader)

    logger.logDebug("bindGameEvent called. | Response: ", response)


def sendGameEvent(game, event, value=None):

    urlPrefix, dataHeader, parsedPortInfo = getAccessInformation()
    urlSteelseriesEngine = urlPrefix + parsedPortInfo["address"] + "/game_event"

    dataPy = { "game": game, "event": event, "data": { "value": value }}
    
    dataJson = json.dumps(dataPy)
    response = requests.post(urlSteelseriesEngine, data = dataJson, headers = dataHeader)
    logger.logDebug("sendGameEvent called. | Response: ", response, " | event value: ", value)


def readSteelseriesEnginePort():
    pathToProgramData = os.getenv("PROGRAMDATA")
    pathToSteelSeriesEngine = os.path.join(pathToProgramData, "SteelSeries", "SteelSeries Engine 3")
    pathToPortInfo = os.path.join(pathToSteelSeriesEngine,"coreProps.json")

    with open(pathToPortInfo) as portInfoFile:
        return json.load(portInfoFile)


def removeEvent(game, event):

    urlPrefix, dataHeader, parsedPortInfo = getAccessInformation()
    urlSteelseriesEngine = urlPrefix + parsedPortInfo["address"] + "/remove_game_event"

    dataPy = { "game": game, "event": event}
    dataJson = json.dumps(dataPy)
    response = requests.post(urlSteelseriesEngine, data = dataJson, headers = dataHeader)
    logger.logDebug("removeEvent called. | Response: ", response)


def bindSpotEvent(game, devicetype, zone, clearOldEvent = False):
    event = cfg["gamesense_config"]["event_spot"]
    min_value = 0
    max_value = 1
    icon_id = 0
    mode = Mode.COLOR

    if clearOldEvent:
        removeEvent(game, event)

    time.sleep(0.5)

    yellow = StaticColor(255,255,0)
    black = StaticColor(0,0,0)
    color = [RangeColor(0,0,black), RangeColor(1,1,yellow)]
    # color = [RangeColor(0,0,StaticColor(0,0,0)), RangeColor(1, 100, GradientColor(zero,hundred))]

    # handlers = [ColorHandler(devicetype, zone, mode, color, rate)]
    handlers = [ColorHandler(devicetype, zone, mode, color)]

    bindGameEvent(game, event, min_value, max_value, icon_id, devicetype, zone, mode, handlers)

    return event


def sendSpotEvent(game, value = None):
    event = cfg["gamesense_config"]["event_spot"]
    sendGameEvent(game, event, value)


def bindReloadEvent(game, devicetype, zone, clearOldEvent):
    event = cfg["gamesense_config"]["event_reload"]
    min_value = 0
    max_value = 100
    icon_id = 0
    mode = Mode.PERCENT

    if clearOldEvent:
        removeEvent(game, event)

    time.sleep(0.5)

    zero = StaticColor(255,0,0)
    hundred = StaticColor(0,255,0)
    color = GradientColor(zero,hundred)
    
    handlers = [ColorHandler(devicetype, zone, mode, color)]

    bindGameEvent(game, event, min_value, max_value, icon_id, devicetype, zone, mode, handlers)

    return event


def sendReloadEvent(game, value = None):
    event = cfg["gamesense_config"]["event_reload"]
    if value != None:
        sendGameEvent(game, event, value)
        # print(logPrefix, "sendReloadEvent called. | value: ", value)


def bindHealthEvent(game, devicetype, zone, clearOldEvent):
    event = cfg["gamesense_config"]["event_health"]
    min_value = 0
    max_value = 100
    icon_id = 0
    mode = Mode.PERCENT

    if clearOldEvent:
        removeEvent(game, event)

    time.sleep(0.5)

    zero = StaticColor(255,0,0)
    hundred = StaticColor(0,255,0)
    color = GradientColor(zero,hundred)
    # color = [RangeColor(0,0,StaticColor(0,0,0)), RangeColor(1, 100, GradientColor(zero,hundred))]

    # handlers = [ColorHandler(devicetype, zone, mode, color, rate)]
    handlers = [ColorHandler(devicetype, zone, mode, color)]

    bindGameEvent(game, event, min_value, max_value, icon_id, devicetype, zone, mode, handlers)

    return event


def sendHealthEvent(game, value = None):
    event = cfg["gamesense_config"]["event_health"]
    sendGameEvent(game, event, value)


def sendHeartbeat(game):
    urlPrefix, dataHeader, parsedPortInfo = getAccessInformation()
    urlSteelseriesEngine = urlPrefix + parsedPortInfo["address"] + "/game_heartbeat"
    dataPy = { "game": game}

    dataJson = json.dumps(dataPy)
    response = requests.post(urlSteelseriesEngine, data = dataJson, headers = dataHeader)
    logger.logTrace("<3 <3 <3 HEARTBEAT <3 <3 <3")


def sendGameMetaData(game, game_display_name, developer):
    urlPrefix, dataHeader, parsedPortInfo = getAccessInformation()
    urlSteelseriesEngine = urlPrefix + parsedPortInfo["address"] + "/game_metadata"
    dataPy = { "game": game, "game_display_name": game_display_name, "developer": developer}

    dataJson = json.dumps(dataPy)
    response = requests.post(urlSteelseriesEngine, data = dataJson, headers = dataHeader)
    logger.logTrace("sent GameSense meta data.")


def sendStopGame(game):
    urlPrefix, dataHeader, parsedPortInfo = getAccessInformation()
    urlSteelseriesEngine = urlPrefix + parsedPortInfo["address"] + "/stop_game"
    dataPy = { "game": game}

    dataJson = json.dumps(dataPy)
    response = requests.post(urlSteelseriesEngine, data = dataJson, headers = dataHeader)
    logger.logTrace("sent GameSense stop game.")

def main():

    game = cfg["gamesense_config"]["game_name"]
    # devicetype = "rgb-103-zone"
    devicetype = cfg["gamesense_config"]["device_type"]
    # zone = "one-hundred-three"
    zone = cfg["gamesense_config"]["zone_health"]
    
    # rate = Rate([RangeFrequency(0, 30, 4),RangeFrequency(31, 50, 2),RangeFrequency(51, 100, 0)], [RangeRepeatLimit(0, 30, 10),RangeRepeatLimit(31, 50, 5),RangeRepeatLimit(51, 100, 1)])
    # rate = Rate(2, [RangeRepeatLimit(31, 50, 5)])
    # zero = StaticColor(0,0,0)
    # hundred = StaticColor(255,255,0)
    # color = StaticColor(255,255,0)
    # color = GradientColor(zero,hundred)
    # color = StaticColor(0,100,100)

    event = bindHealthEvent(game, devicetype, zone, False)

    value = 5

    count = 10
    while count:
        sendGameEvent(game, event, value)
        # time.sleep(2.0)
        count-=1
        value += 10


if __name__ == "__main__":
    main()