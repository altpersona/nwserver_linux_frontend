#!/bin/bash

#MODNAME=PRC8_Tester

pushd /home/user/.steam/steam/steamapps/common/Neverwinter Nights/bin/linux-x86

#export NWNX_CORE_SKIP_ALL=n
#export NWNX_CORE_LOAD_PATH=./unified/Binaries
#export NWNX_CORE_LOG_LEVEL=6

#export NWNX_SERVERLOGREDIRECTOR_SKIP=n
#export NWNX_SERVERLOGREDIRECTOR_LOG_LEVEL=6

# Only SQLite is supported out of the box
#export NWNX_SQL_SKIP=y
#export NWNX_SQL_TYPE=SQLITE

# Redis needs additional configuration, see the Extra header in the readme
#export NWNX_REDIS_SKIP=y
#export NWNX_REDIS_HOST=localhost

# These plugins should all work, enable when needed
# You can check a plugin's README for additional environment variables you can set:
# https://github.com/nwnxee/unified/tree/master/Plugins
#export NWNX_ADMINISTRATION_SKIP=n
#export NWNX_APPEARANCE_SKIP=n
#export NWNX_AREA_SKIP=n
#export NWNX_CHAT_SKIP=y
#export NWNX_CREATURE_SKIP=n
#export NWNX_DAMAGE_SKIP=y
#export NWNX_DIALOG_SKIP=n
#export NWNX_ELC_SKIP=y
#export NWNX_EFFECT_SKIP=n
#export NWNX_ENCOUNTER_SKIP=n
#export NWNX_EVENTS_SKIP=n
#export NWNX_FEAT_SKIP=n
#export NWNX_FEEDBACK_SKIP=y
#export NWNX_ITEM_SKIP=y
#export NWNX_ITEMPROPERTY_SKIP=y
#export NWNX_MAXLEVEL_SKIP=n
#export NWNX_NOSTACK_SKIP=n
#export NWNX_OBJECT_SKIP=n
#export NWNX_OPTIMIZATIONS_SKIP=n
#export NWNX_PLAYER_SKIP=n
#export NWNX_RACE_SKIP=n
#export NWNX_RENAME_SKIP=n
#export NWNX_REVEAL_SKIP=n
#export NWNX_SKILLRANKS_SKIP=n
#export NWNX_THREADWATCHDOG_SKIP=y
#export NWNX_TILESET_SKIP=n
#export NWNX_TWEAKS_SKIP=n
#export NWNX_UTIL_SKIP=n
#export NWNX_VISIBILITY_SKIP=n
#export NWNX_WEAPON_SKIP=n
#export NWNX_WEBHOOK_SKIP=y

# These plugins are missing dependencies or outside configuration and won't work out of the box
#export NWNX_DOTNET_SKIP=y
#export NWNX_LUA_SKIP=y
#export NWNX_METRICS_INFLUXDB_SKIP=y
#export NWNX_PROFILER_SKIP=y
#export NWNX_RUBY_SKIP=y
#export NWNX_SPELLCHECKER_SKIP=y
#export NWNX_TRACKING_SKIP=y

LD_PRELOAD=~/unified/Binaries/NWNX_Core.so \
 ./nwserver-linux \
  -module "test_module" \
  -maxclients 12 \
  -minlevel 1 \
  -maxlevel 60 \
  -pauseandplay 0 \
  -pvp 2 \
  -servervault 1 \
  -elc 1 \
  -ilr 1 \
  -gametype 3 \
  -oneparty 0 \
  -difficulty 4 \
  -autosaveinterval 0 \
  -playerpassword '' \
  -dmpassword '' \
  -servername "Tester Server" \
  -publicserver 1 \
  -reloadwhenempty 0 \
  -port 5120 \
  -userdirectory /home/user/Documents/Neverwinter Nights \
#  -nwsyncurl http://localhost:5120/nwsync \
popd