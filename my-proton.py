#!/usr/bin/python3


manual = """
This program allows you to run any exe files in a custom wine prefix.

See README.md for instruction.
"""

import os
import subprocess
import sys
import argparse
from envcalc import envcalc, add_wine_prefix

parser = argparse.ArgumentParser(
                    prog='Simple Proton wrapper',
                    description=manual,
                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('prefixname', help='The name of wineprefix. The wineprefix should be placed at `~/wineprefix/[wineprefix name]`')

parser.add_argument('args', nargs='*', help='Args to be passed on wine or executed directly')

parser.add_argument('-l', '--lang', help="wine language", default='ja_JP.UTF-8')

parser.add_argument('--runtime', help="Specify steam linux runtime container executable path relative to steamapps.", default='SteamLinuxRuntime_sniper/_v2-entry-point')

parser.add_argument('--proton', help="Specify Proton Version the path relative to steamapps.", default='Proton - Experimental')

parser.add_argument('-s', '--preset_sniper', help="path to the preset file, relative to this script.", default='preset_sniper_wide')

parser.add_argument('-e', '--preset_exe', help="path to the preset file, relative to this script.", default='preset_exe_wide')

parser.add_argument('--dumpenvs_sniper', help="Specify path to dumped env file for sniper. (Can be obtained by adding 'cat /proc/$$/environ > $HOME/my-proton-tools/dumpenvs_sniper' to '$HOME/.local/share/Steam/steamapps/common/SteamLinuxRuntime_sniper/_v2-entry-point')", default='dumpenvs_sniper')

parser.add_argument('--dumpenvs_exe', help="Specify path to dumped env file for exe files. (Can be obtained by running 'cat /proc/12345/environ > $HOME/my-proton-tools/dumpenvs_exe', where 12345 is the pid of the windows exe)", default='dumpenvs_exe')

parser.add_argument('-r', help="execute raw command such as `winetricks` or `wineserver -k`", action='store_true')

args_r_remain: list[str] = []

if '-r' in sys.argv:
    args_r_index = sys.argv.index('-r')
    args = parser.parse_args(sys.argv[1:args_r_index+1])
    args_r_remain = sys.argv[args_r_index+1:]
else:
    args = parser.parse_args()

sniper_path: str = os.path.expanduser('~/.local/share/Steam/steamapps/common/%s' % args.runtime)

tool_path = os.path.abspath(os.path.dirname(__file__))

proton_root: str = os.path.expanduser("~/.local/share/Steam/steamapps/common/%s/" % args.proton)
if not os.path.exists(proton_root):
    proton_root = "/usr/share/steam/compatibilitytools.d/proton"
    if not os.path.exists(proton_root):
        raise FileNotFoundError('Proton executable not found.')

calc_env_sniper = envcalc(args.dumpenvs_sniper, args.prefixname, args.preset_sniper, args.lang, "SNIPER")
proc_env_sniper = os.environb.copy()
proc_env_sniper.update(calc_env_sniper)

calc_env_exe = add_wine_prefix(envcalc(args.dumpenvs_exe, args.prefixname, args.preset_exe, args.lang, "EXE"), args.prefixname)

proc_args: list[str] = []

if len(args_r_remain) > 0:
    proc_args = args_r_remain
else:
    winepath = os.path.join(proton_root, 'files', 'bin', 'wine')
    if not os.path.exists(winepath):
        winepath = os.path.join(proton_root, 'dist', 'bin', 'wine')
    proc_args = [winepath] + args.args

import pickle
with open(os.path.join(tool_path, 'inner', 'arg-pickle'), 'wb') as f:
    pickle.dump([proc_args, calc_env_exe], f)

subprocess.run([sniper_path, os.path.join(tool_path, 'inner', 'my-proton-inner.py')], env=proc_env_sniper)

