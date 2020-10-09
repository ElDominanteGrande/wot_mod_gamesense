import os
import json

Config = {
    "repo_info":{
        "name": "wot_mod_gamesense",
        "author": "ElDominanteGrande",
        "maintainer": "ElDominanteGrande",
        "credits": ["ElDominanteGrande"],
        "copyright": "Copyright 2020, ElDominanteGrande",
        "license": "MIT",
        "version": "1.0.2",
        "email": "",
        "status": "Production"
    },

    "gamesense_config":{
        "game_name": "WORLDOFTANKS",
        "game_nameHR": "World of Tanks",
        "event_health": "HEALTH",
        "event_reload": "RELOAD",
        "event_spot": "SPOT",
        "device_type": "rgb-zoned-device",
        "zone_health": "one",
        "zone_spot": "two",
        "zone_reload": "three",
        "clear_events_on_init": False
    },

    "code_config":{
        "log_prefix": "[mod_GameSense] ",
        "log_level": 1
    }
}
