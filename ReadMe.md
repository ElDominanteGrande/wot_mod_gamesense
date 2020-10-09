# WoT_Mod_GameSense

WoT_Mod_GameSense is a modification for the online game World of Tanks enhancing the player experience by making use of the SteelSeries  GameSense SDK.

Any hardware capable of GameSense can be used to display in-game states like health, reload time and so on.

## Installation

Clone this repo.

## Usage

Assure you have a device capable of GameSense and RGB zones connected. Further, SteelSeries Engine must be installed and running on your system. This software can be downloaded [here](https://steelseries.com/engine).
Otherwise this mod won't work.

### Either:

Download the .wotmod file from the releases of this repository and copy it to the mods folder of your World of Tanks installation.

```bash
<WorldOfTanks-install-path>\mods\<current-WorldOfTanks-version>
```

### Or:

Build the .wotmod file by executing the following script using Python 2.7:

```bash
<Repo-folder>\utils\build_mod.py
```

Be sure to change the configuration for the build according to your system (installation path of World of Tanks) and if you want to deploy the created .wotmod file instantly to your World of Tanks installation.
See configuration here:

```bash
<Repo-folder>\utils\config.json
```

Copy the built .wotmod file from the generated build folder to the mods folder of your World of Tanks installation path, if deploying was not done by the build step before.

Start World of Tanks. Load into a match or start a replay to let the mod register the GameSense events.

Configure the registered GameSense events, the zones to be used and their colors in the SteelSeries Engine software (GUI).

Any hardware capable of GameSense should be displaying the configured events and states (e.g.: health, reload time and spotted indicator) on its LEDs.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to test your changes using replays.

## Copyright and License Information

MIT License

Copyright (c) 2020 ElDominanteGrande

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.