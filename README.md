# My Proton Tools

This script enables you to run any executable files in proton environment.

Please note that proton is highly unstable for simpler or older games (renpy, rpg maker etc). For that purpose I recommend usual wine.

## Installation
Requires Python 3.11, Steam, Steam Linux Runtime installed via Steam, Proton installed via Steam.

Tested in Arch Linux and Ubuntu with XFCE. Both snap and direct installation of steam supported.

## Instruction

`my-proton.py` is the main script. You need to generate `dumpenvs` before running it. The following instruction supposes that this tool is placed in `$HOME/my-proton-tools`. If Steam is installed via snap, every command should be run in the `snap run --shell steam` shell environment.

1. Search for the sniper/runtime path and edit it. It uses entrypoint V2 by default. Specify `--runtime` commandline argument to override entrypoint and Steam Linux Runtime version.
    1. Entrypoint V1: Append `cat /proc/$$/environ > $HOME/my-proton-tools/dumpenvs_sniper_v1` to `$HOME/.local/share/Steam/steamapps/common/SteamLinuxRuntime_sniper/run`
    2. Entrypoint V2: Append `cat /proc/$$/environ > $HOME/my-proton-tools/dumpenvs_sniper` to `$HOME/.local/share/Steam/steamapps/common/SteamLinuxRuntime_sniper/_v2-entry-point`
2. Start a steam app via proton, and get its pid.
3. `cat /proc/[pid of the game]/environ > $HOME/my-proton-tools/dumpenvs_exe`
4. Create prefix files, or copy example prefix files (`preset_sniper_wide` and `preset_exe_wide`) from the `example_presets` directory, which has different prefix files depending on whether Steam is directly installed or installed via snap.  
   Guide on how to create a prefix file:
    1. Run this program once and generate `dumpenvs_EXE_keys_values` and `dumpenvs_SNIPER_keys_values`
    2. Copy `dumpenvs_EXE_keys_values`/`dumpenvs_SNIPER_keys_values` and rename them to something else.
    3. In the copied files, replace string values next to the keys with 'v', 'p', 'c' or 'd' or delete the line, so that we can successfully load the environment variables required to run wine.
    ```
    v = keep value
    c = create cache dir
    d = delete value (same as just deleting the line)
    a = append value
    p = prepend value
    ```
    4. by passing `-s` (for sniper/runtime) or `-e` (for exe) argument, specify the path of edited files, relative to the tool location.
5. `mkdir $HOME/wineprefix`
6. Run `create-prefix.sh` to safely create a new proton environment. (Please edit `SAMPLEAPPID` to specify the steam game id that you have previously played and is a windows-only game)

You can change proton version by specifying `--proton` and `--runtime` simultaneously. Also, if you use multiple proton versions / runtime versions / runtime entrypoint executables, please dump different dumpenv files, and change `-s` and `-e` accordingly.

