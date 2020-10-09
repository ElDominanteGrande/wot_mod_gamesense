import sys, os

from gui.gamesense import steelseries_gamesense
import steelseries_gamesense
import threading
import time
import Threads
import mod_gamesense_logger as logger
from config import Config as cfg

class Controller(object):

    def __init__(self):
        
        # Controller configuration
        self.CtrlConfig_ClearOldGameSenseEvents = cfg["gamesense_config"]["clear_events_on_init"]

        # Controller state
        self.CtrlState_isInitialized = False
        self.CtrlState_prevTimeLeft = 0.0
        self.CtrlState_prevTimestamp = 0.0

        # SteelSeries GameSense properties
        self.GameSense_Name = cfg["gamesense_config"]["game_name"]
        self.GameSense_NameHR = cfg["gamesense_config"]["game_nameHR"]
        self.GameSense_DeviceType = cfg["gamesense_config"]["device_type"]
        self.GameSense_ZoneHealth = cfg["gamesense_config"]["zone_health"]
        self.GameSense_ZoneSpot = cfg["gamesense_config"]["zone_spot"]
        self.GameSense_ZoneReload = cfg["gamesense_config"]["zone_reload"]

        # global thread objects
        self.Thread_KeepAlive = None
        self.Thread_ResetSpotIndicator = None
        self.Thread_UpdateReloadIndicator = None

        Threads.GameSense_Name = self.GameSense_Name

        return


    def onHealthChanged(self, newHealth, maxHealth):
        value = int(((float)(newHealth)/(float)(maxHealth))*100)
        steelseries_gamesense.sendHealthEvent(self.GameSense_Name, value)
        logger.logDebug("onHealthChanged called. | max health: ", maxHealth, " | ", newHealth, " event value: ", value)


    def onEnterWorld(self):
        """
        The game starts and evrything gets initialized.
        """

        logger.logTrace("onEnterWorld called.")
        logger.logDebug("Exe: ", sys.executable, "Import module search path: ", os.__file__)

        # Initialize GameSense events
        if not self.CtrlState_isInitialized:
            self.CtrlState_isInitialized = True
            steelseries_gamesense.readSteelseriesEnginePort.logged = False

            # bind events
            steelseries_gamesense.bindHealthEvent(self.GameSense_Name, self.GameSense_DeviceType, self.GameSense_ZoneHealth, self.CtrlConfig_ClearOldGameSenseEvents)
            steelseries_gamesense.bindSpotEvent(self.GameSense_Name, self.GameSense_DeviceType, self.GameSense_ZoneSpot, self.CtrlConfig_ClearOldGameSenseEvents)
            steelseries_gamesense.bindReloadEvent(self.GameSense_Name, self.GameSense_DeviceType, self.GameSense_ZoneReload, self.CtrlConfig_ClearOldGameSenseEvents)

            # send init values for events
            steelseries_gamesense.sendSpotEvent(self.GameSense_Name, 0)
            steelseries_gamesense.sendReloadEvent(self.GameSense_Name, 100)
            steelseries_gamesense.sendHealthEvent(self.GameSense_Name, 100)

            # send meta data
            steelseries_gamesense.sendGameMetaData(self.GameSense_Name, self.GameSense_NameHR, cfg["repo_info"]["author"])

        # Start a thread for heartbeats to GameSense
        if not self.Thread_KeepAlive:
            self.Thread_KeepAlive = threading.Thread(target=Threads.keepGameSenseAlive, args=())
            self.Thread_KeepAlive.start()
            logger.logTrace("keepAliveThread started.")


    def onLeaveWorld(self):
        # print(logPrefix + "onLeaveWorld called.")

        self.CtrlState_isInitialized = False
        self.CtrlState_prevTimeLeft = 0.0
        self.CtrlState_prevTimestamp = 0.0

        if self.Thread_KeepAlive:
            Threads.keepGameSenseAlive.terminate = True
            self.Thread_KeepAlive = None
            logger.logTrace("keepAliveThread stopped.")

        if self.Thread_ResetSpotIndicator:
            Threads.resetSpotIndicator.terminate = True
            self.Thread_ResetSpotIndicator = None
            logger.logTrace("resetSpotIndicatorThread stopped.")

        if self.Thread_UpdateReloadIndicator:
            Threads.updateReloadIndicator.terminate = True
            self.Thread_UpdateReloadIndicator = None
            logger.logTrace("updateReloadIndicatorThread stopped.")

        # stop GameSense game
        steelseries_gamesense.sendStopGame(self.GameSense_Name)


    def showSixthSenseIndicator(self):
        steelseries_gamesense.sendSpotEvent(self.GameSense_Name, 1)
        self.Thread_ResetSpotIndicator = threading.Thread(target=Threads.resetSpotIndicator, args=())
        self.Thread_ResetSpotIndicator.start()

        logger.logTrace("resetSpotIndicatorThread started.")


    def updateVehicleGunReloadTime(self, timeLeft, baseTime):
        epsilon = 0.001
        currentTimeSec = lambda: time.time()    
        
        # Sometimes this function gets called with a timeLeft value which can't be correct (e.g: 0 even if it just started reloading).
        # Therefore only update the timeLeft value when it's greater than 0(+ epsilon).
        # Or when it's 0 but then the time passed since the last update must be greater than the difference of the new and old timeLeft values.
        if ( (abs(timeLeft) >= epsilon) or (abs(self.CtrlState_prevTimeLeft-timeLeft) <= abs(currentTimeSec() - self.CtrlState_prevTimestamp + epsilon)) ):
            logger.logDebug("updateVehicleGunReloadTime called. | reload time left: ", timeLeft, " entire reload time: ", baseTime)

            # Send new info to thread
            Threads.updateReloadIndicator.timeLeft = timeLeft
            Threads.updateReloadIndicator.updateTimeLeft = True

            # update local values for further calculation
            self.CtrlState_prevTimestamp = currentTimeSec()
            self.CtrlState_prevTimeLeft = timeLeft

        # Send new info to thread
        Threads.updateReloadIndicator.baseTime = baseTime

        # When there is no thread for the reload indicator already running, start a new one.
        # Should only happen on the first call of this method.
        if not self.Thread_UpdateReloadIndicator:
            self.Thread_UpdateReloadIndicator = threading.Thread(target=Threads.updateReloadIndicator, args=())
            self.Thread_UpdateReloadIndicator.start()

            logger.logTrace("updateReloadIndicatorThread started.")


    def __del__(self):
        self.onLeaveWorld()