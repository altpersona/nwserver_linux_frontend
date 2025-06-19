# This file documents the forked changes made to the original nwserver-linux frontend.

## Forked by: <your name or handle here>

## Date: 2025-06-19

### Summary of changes:

- Added support for specifying the working directory as the directory containing the nwserver-linux binary, not the user directory.
- User directory is now passed as an argument if needed, not used as the working directory.
- Added missing PyQt5 widget imports to resolve lint errors.
- Added UI fields for all server options, including module path, port, and public server.
- Arranged checkboxes in two columns for a more compact UI.
- Made the log output window resizable by placing it in a QSplitter with the rest of the main widgets.
- Fixed argument mapping for server compatibility:
  - Difficulty dropdown now maps to values 1–4.
  - Local/server characters now use -servervault 0/1 instead of -localchars.
  - Boolean flags (elc, ilr, oneparty, reloadwhenempty) now use 0/1.
  - Module argument now passes only the module name (no path or .mod extension).
  - PvP and Game Type now use integer values as required by the server.
- Removed the Player Pause option from the UI and command-line arguments, as it is not supported by nwserver.
- Replaced the non-standard -userdir argument with -userdirectory to match the official server options and reference documentation.
- Added support for advanced options:
  - NWSync URL (-nwsyncurl)
  - NWSync Hash (-nwsynchash)
  - NWSync Publish HAKs (-nwsyncpublishhaks)
  - Quiet Mode (-quiet)
  - Interactive Mode (-interactive)
    All are now available in the GUI and passed to the server if set.

### How to use this fork:

- Select the nwserver-linux binary and the user directory as needed.
- All server options can be set via the GUI and will be passed to the server on launch.

---

This file serves as a manifest of the forked changes. For further details, see the code and commit history.
