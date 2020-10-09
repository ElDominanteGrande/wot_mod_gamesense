import time
import steelseries_gamesense
import mod_gamesense_logger as logger

GameSense_Name = ""

def updateReloadIndicator():
    """
    This function is run as a thread and updates the reload indicator of GameSense.
    """
    updateReloadIndicator.terminate = False
    updateReloadIndicator.updateTimeLeft = True
    
    if not hasattr(updateReloadIndicator, "timeLeft"):
        updateReloadIndicator.timeLeft = 0.0
    if not hasattr(updateReloadIndicator, "baseTime"):
        updateReloadIndicator.baseTime = 1.0

    currentTimeSec = lambda: time.time()
    prevTime = currentTimeSec()

    logger.logTrace("thread started: updateReloadIndicator.")

    while not updateReloadIndicator.terminate:
        # Only update the timeLeft value when told to do so.
        if updateReloadIndicator.updateTimeLeft:
            updateReloadIndicator.updateTimeLeft = False
            localTimeLeft = updateReloadIndicator.timeLeft
            logger.logDebug("updateReloadIndicator called. | Updated updateReloadIndicator.timeLeft: ", updateReloadIndicator.timeLeft, " | updateReloadIndicator.baseTime: ", updateReloadIndicator.baseTime, "| localTimeLeft: ", localTimeLeft)

        # Update baseTime value everytime
        localbaseTime = updateReloadIndicator.baseTime

        # Clip value between 0 and 100 for GameSense event
        value = min(max(0, 100-(((float)(localTimeLeft)/(float)(localbaseTime)) * 100)), 100)

        logger.logDebug("updateReloadIndicator called. | updateReloadIndicator.timeLeft: ", localTimeLeft, "updateReloadIndicator.baseTime: ", localbaseTime, "value: ", value)

        # Send event
        steelseries_gamesense.sendReloadEvent(GameSense_Name, value)

        # Calculate and update the local values for the next computation.
        localTimeLeft = max(0, localTimeLeft - (currentTimeSec() - prevTime))
        prevTime = currentTimeSec()

    logger.logTrace("thread finished: updateReloadIndicator.")


def resetSpotIndicator():
    """
    This function is run as a thread and unsets the spot indicator of GameSense after a given wait time (in seconds).
    """
    resetSpotIndicator.terminate = False

    deltaSleep = 0.1
    epsilon = 0.001
    waitTime = 10.0

    currentTimeSec = lambda: time.time()
    startTime = currentTimeSec()

    while (abs((currentTimeSec() - startTime) <= abs(waitTime - epsilon))) and not resetSpotIndicator.terminate:
        time.sleep(deltaSleep)

    steelseries_gamesense.sendSpotEvent(GameSense_Name, 0)
    logger.logTrace("thread finished: resetSpotIndicator.")

def keepGameSenseAlive():

    keepGameSenseAlive.terminate = False

    waitTime = 10.0

    while not keepGameSenseAlive.terminate:
        steelseries_gamesense.sendHeartbeat(GameSense_Name)
        time.sleep(waitTime)

    logger.logTrace("thread finished: keepGameSenseAlive.")