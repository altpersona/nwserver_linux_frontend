# Neverwinter Nights Server Frontend

A PyQt5-based GUI application for managing and configuring Neverwinter Nights Enhanced Edition dedicated servers on Linux systems.

## Features

- **Easy Server Configuration**: Intuitive GUI for all server settings
- **Module Management**: Load custom modules with automatic path detection
- **Save Game Support**: Load existing save games with slot management
- **Real-time Output**: Live server console output with highlighted messages
- **Persistent Settings**: Automatically saves and restores all configuration settings
- **Path Validation**: Validates module paths using `nwn.ini` configuration
- **NWSync Support**: Configure NWSync URL, hash, and publishing options
- **Password Protection**: Support for player, DM, and admin passwords
- **Advanced Options**: Difficulty, level restrictions, PvP modes, and more

## Requirements

- **Python 3.x** with PyQt5
- **Neverwinter Nights Enhanced Edition** with Linux server binary (`nwserver-linux`)
- **Linux system** (native Linux, WSL, or other Unix-like environments)

### Installing Dependencies

#### Ubuntu/Debian:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-pyqt5
```

#### Fedora/RHEL:

```bash
sudo dnf install python3 python3-pip python3-qt5
```

#### Arch Linux:

```bash
sudo pacman -S python python-pip python-pyqt5
```

## Installation

1. **Clone or download** this repository
2. **Install PyQt5** using your system's package manager (see above)
3. **Locate your NWN installation** and note the path to `nwserver-linux`

## Usage

### Starting the Application

```bash
python3 nwserver_frontend.py
```

### Initial Setup

1. **Set NWServer Path**: Browse to your `nwserver-linux` binary location

   - Typically: `/path/to/steam/steamapps/common/Neverwinter Nights/bin/linux-x86/nwserver-linux`

2. **Set User Directory**: Choose where NWN will store user data

   - Example: `/home/username/.local/share/Neverwinter Nights`
   - This creates subdirectories for modules, saves, logs, etc.

3. **Configure Server Settings**:
   - Server name, difficulty, player limits
   - Passwords, PvP settings, character restrictions
   - Module selection and save game options

### Server Configuration

#### Basic Settings

- **Server Name**: How your server appears in multiplayer listings
- **Difficulty**: Easy, Normal, D&D Hardcore, Very Difficult
- **Player Limits**: Maximum clients, level restrictions
- **Game Type**: Which lobby your server appears in

#### Module & Save Games

- **Module**: Select a custom module (`.mod` file) to run
- **Save Game**: Load an existing save game instead of a fresh module
- **Slot Number**: Save game slot to use

#### Network & Security

- **Port**: Server port (default 5121)
- **Public Server**: Whether to list on public servers
- **Passwords**: Player, DM, and Admin access control

#### Advanced Options

- **Server Vault**: Force server-stored characters vs local characters
- **Legal Characters**: Enforce character creation rules
- **Item Restrictions**: Enforce item level restrictions
- **Party Options**: Single party vs multiple parties
- **Auto-save**: Automatic save interval in minutes

### NWSync Configuration

NWSync allows automatic content downloading for players:

- **NWSync URL**: Base URL for your content repository
- **NWSync Hash**: Specific manifest hash (auto-fetched if not provided)
- **Publish HAKs**: Whether to advertise HAK list alongside NWSync

### Running the Server

1. **Configure all settings** as desired
2. **Click "Start Server"** to launch
3. **Monitor output** in the console window
4. **Look for highlighted messages** showing working directories
5. **Click "Stop Server"** to shut down gracefully

## File Structure

The application creates/uses these files:

```
nwserver_linux_frontend/
├── nwserver_frontend.py       # Main application
├── nwserver_frontend.ini      # Saved configuration
├── resources/
│   ├── .rodata.cleaned.txt    # Server documentation reference
│   └── clean_rodata.py        # Utility script
└── README.md                  # This file
```

## Troubleshooting

### Module Not Found

- Verify module exists in user directory: `<userdirectory>/modules/modulename.mod`
- Check the `nwn.ini` file in your user directory for correct paths
- Ensure module name matches exactly (case-sensitive on Linux)

### Server Won't Start

- Verify `nwserver-linux` binary path is correct
- Check file permissions on the server binary
- Ensure user directory is writable
- Look for error messages in the console output

### Directory Issues

- The application reads `nwn.ini` to find correct module paths
- User directory should contain subdirectories like `modules/`, `saves/`, etc.
- Check highlighted "Working Directory" messages in server output

### Network Issues

- Default port is 5121, ensure it's not in use
- Check firewall settings for the chosen port
- For public servers, ensure port forwarding is configured

## Configuration Files

### nwn.ini Location

The server looks for `nwn.ini` in the user directory to determine resource paths:

```
<userdirectory>/nwn.ini
```

### Saved Settings

All GUI settings are automatically saved to:

```
nwserver_frontend.ini
```

## Command Line Reference

The application generates command lines like:

```bash
./nwserver-linux -userdirectory "/path/to/user/dir" -module "modulename" -difficulty 2 -maxclients 8 -port 5121
```

For complete command line options, see `resources/.rodata.cleaned.txt` or run:

```bash
./nwserver-linux -help
```

## Contributing

This is an open-source project. Feel free to:

- Report bugs or issues
- Suggest new features
- Submit pull requests
- Improve documentation

## License

This project is provided as-is for the Neverwinter Nights community.

## Acknowledgments

- **BioWare/Beamdog** for Neverwinter Nights Enhanced Edition
- **The NWN Community** for continued support and development
- Built using **PyQt5** for the GUI framework
