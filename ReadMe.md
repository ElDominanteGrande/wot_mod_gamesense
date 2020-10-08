# WoT_Mod_GameSense

WoT_Mod_GameSense is a modification for the online game World of Tanks enhancing the player experience by making use of the SteelSeries  GameSense SDK.

Any hardware capable of GameSense can be used to display in-game states like health, reload time and so on.

## Installation

Clone this repo.

## Usage

Build the .wotmod file by executing the following script using Python 2.7:

```bash
<Repo-folder>\utils\build_mod.py
```

Then copy the .wotmod file from the generated build folder to the mods folder of your World of Tanks installation path.

```bash
<WorldOfTanks-install-path>\mods\<current-WorldOfTanks-version>
```

Start World of Tanks.

Configure the registered GameSense events and the zones to be used in the SteelSeries Engine software (GUI).

Load into a match and any hardware capable of GameSense should be displaying the configured events and states (e.g.: health, reload time and spotted indicator) on its LEDs.

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