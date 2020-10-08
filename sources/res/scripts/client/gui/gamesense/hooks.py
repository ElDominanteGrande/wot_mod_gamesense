import sys, os
import threading
import time

from Vehicle import Vehicle
from gui.Scaleform.daapi.view.battle.shared.indicators import SixthSenseIndicator
from Avatar import PlayerAvatar

from utils import override
import steelseries_gamesense
import Controller
import mod_gamesense_logger as logger

__all__ = ()

_Controller = Controller.Controller()


@override(Vehicle, 'onHealthChanged')
def onHealthChanged(baseMethod, baseObject, newHealth, attackerID, attackReasonID):
    if baseObject.isPlayerVehicle:
        _Controller.onHealthChanged(newHealth, baseObject.maxHealth)

    baseMethod(baseObject, newHealth, attackerID, attackReasonID)    


@override(Vehicle, 'onEnterWorld')
def onEnterWorld(baseMethod, baseObject, preregs):
    """
    The game starts and evrything gets initialized.
    """
    baseMethod(baseObject, preregs)
    isPlayerVehicle = False

    try:
        isPlayerVehicle = getattr(baseObject, "isPlayerVehicle")
    except:
        logger.logDebug("onEnterWorld called. | No attribute 'isPlayerVehicle'.")

    # Initialize GameSense events
    if isPlayerVehicle:
        logger.logTrace("onEnterWorld called.")
        _Controller.onEnterWorld()


@override(Vehicle, 'onLeaveWorld')
def onLeaveWorld(baseMethod, baseObject):
    baseMethod(baseObject)

    isPlayerVehicle = False

    try:
        isPlayerVehicle = getattr(baseObject, "isPlayerVehicle")
    except:
        logger.logDebug("onLeaveWorld called. | No attribute 'isPlayerVehicle'.")

    # print(logPrefix + "onLeaveWorld called.")

    if isPlayerVehicle:
        _Controller.onLeaveWorld()

    
@override(Vehicle, '__del__')
def __del__(baseMethod, baseObject):
    isPlayerVehicle = False

    try:
        isPlayerVehicle = getattr(baseObject, "isPlayerVehicle")
    except:
        logger.logDebug("__del__ called. | No attribute 'isPlayerVehicle'.")

    if isPlayerVehicle:
        logger.logTrace("__del__ called.")
        _Controller.onLeaveWorld()

    baseMethod(baseObject)


@override(SixthSenseIndicator, 'as_showS')
def showSixthSenseIndicator(baseMethod, baseObject):
    _Controller.showSixthSenseIndicator()

    logger.logTrace("showSixthSenseIndicator called.")

    return baseMethod(baseObject)


@override(PlayerAvatar, 'updateVehicleGunReloadTime')
def updateVehicleGunReloadTime(baseMethod, baseObject, vehicleID, timeLeft, baseTime):
    _Controller.updateVehicleGunReloadTime(timeLeft, baseTime)

    # Execute the original/overridden method
    baseMethod(baseObject, vehicleID, timeLeft, baseTime)
