import sys
import subprocess
import os
import configparser
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QComboBox, QSpinBox, QCheckBox, QFileDialog, QTextEdit, QGroupBox, QGridLayout, QSplitter
)
from PyQt5.QtCore import Qt, QTimer

class NWServerFrontend(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('NWServer-Linux Frontend')
        self.init_ui()
        self.process = None
        self.config_file = os.path.join(os.path.dirname(__file__), 'nwserver_frontend.ini')
        self.load_config()

    def init_ui(self):
        layout = QVBoxLayout()

        # Server options
        options_group = QGroupBox('Server Options')
        options_layout = QGridLayout()

        # Server Name
        options_layout.addWidget(QLabel('Server Name:'), 0, 0)
        self.server_name = QLineEdit('Server')
        options_layout.addWidget(self.server_name, 0, 1)

        # Difficulty
        options_layout.addWidget(QLabel('Difficulty:'), 1, 0)
        self.difficulty = QComboBox()
        self.difficulty.addItems(['Easy', 'Normal', 'Hardcore', 'Very Difficult'])
        options_layout.addWidget(self.difficulty, 1, 1)

        # Autosave Interval
        options_layout.addWidget(QLabel('Autosave (min):'), 2, 0)
        self.autosave = QSpinBox()
        self.autosave.setRange(0, 120)
        options_layout.addWidget(self.autosave, 2, 1)

        # Levels
        options_layout.addWidget(QLabel('Levels:'), 3, 0)
        self.level_min = QSpinBox()
        self.level_min.setRange(1, 40)
        self.level_max = QSpinBox()
        self.level_max.setRange(1, 40)
        self.level_max.setValue(40)
        level_layout = QHBoxLayout()
        level_layout.addWidget(self.level_min)
        level_layout.addWidget(QLabel('to'))
        level_layout.addWidget(self.level_max)
        options_layout.addLayout(level_layout, 3, 1)

        # Max Players
        options_layout.addWidget(QLabel('Max Players:'), 4, 0)
        self.max_players = QSpinBox()
        self.max_players.setRange(1, 255)
        self.max_players.setValue(6)
        options_layout.addWidget(self.max_players, 4, 1)

        # Checkboxes (2 columns)
        self.local_chars = QCheckBox('Local Characters Allowed')
        self.legal_chars = QCheckBox('Enforce Legal Characters')
        self.item_restrict = QCheckBox('Item Level Restrictions')
        self.one_party = QCheckBox('Only One Party')
        self.reload_empty = QCheckBox('Reload When Empty')
        self.local_chars.setChecked(True)
        self.one_party.setChecked(True)
        # Place checkboxes in 2 columns
        options_layout.addWidget(self.local_chars, 5, 0)
        options_layout.addWidget(self.legal_chars, 5, 1)
        options_layout.addWidget(self.item_restrict, 6, 0)
        options_layout.addWidget(self.one_party, 6, 1)
        options_layout.addWidget(self.reload_empty, 7, 1)

        # Module Path
        options_layout.addWidget(QLabel('Module Path:'), 11, 0)
        self.module_path = QLineEdit()
        options_layout.addWidget(self.module_path, 11, 1)
        self.module_path_btn = QPushButton('Browse')
        self.module_path_btn.clicked.connect(self.browse_module_path)
        options_layout.addWidget(self.module_path_btn, 11, 2)

        # Game Type
        options_layout.addWidget(QLabel('Game Type:'), 12, 0)
        self.game_type = QComboBox()
        self.game_type.addItems(['Action', 'Story', 'Custom'])
        options_layout.addWidget(self.game_type, 12, 1)

        # Player vs. Player
        options_layout.addWidget(QLabel('Player vs. Player:'), 13, 0)
        self.pvp_type = QComboBox()
        self.pvp_type.addItems(['None', 'Party', 'Full'])
        options_layout.addWidget(self.pvp_type, 13, 1)

        # Player Password
        options_layout.addWidget(QLabel('Player Password:'), 14, 0)
        self.player_password = QLineEdit()
        options_layout.addWidget(self.player_password, 14, 1)

        # DM Password
        options_layout.addWidget(QLabel('DM Password:'), 15, 0)
        self.dm_password = QLineEdit()
        options_layout.addWidget(self.dm_password, 15, 1)

        # Server Admin Password
        options_layout.addWidget(QLabel('Server Admin Password:'), 16, 0)
        self.admin_password = QLineEdit()
        options_layout.addWidget(self.admin_password, 16, 1)

        # Server Message
        options_layout.addWidget(QLabel('Server Message:'), 17, 0)
        self.server_message = QLineEdit()
        options_layout.addWidget(self.server_message, 17, 1)

        # Save Game Path
        options_layout.addWidget(QLabel('Save Game:'), 18, 0)
        self.save_game = QLineEdit()
        options_layout.addWidget(self.save_game, 18, 1)
        self.save_game_btn = QPushButton('Browse')
        self.save_game_btn.clicked.connect(self.browse_save_game)
        options_layout.addWidget(self.save_game_btn, 18, 2)

        # Slot Number
        options_layout.addWidget(QLabel('Slot Number:'), 19, 0)
        self.slot_number = QSpinBox()
        self.slot_number.setRange(0, 99)
        options_layout.addWidget(self.slot_number, 19, 1)

        # Public Server (Post Game To Internet)
        options_layout.addWidget(QLabel('Post Game To Internet:'), 20, 0)
        self.public_server = QCheckBox()
        self.public_server.setChecked(True)
        options_layout.addWidget(self.public_server, 20, 1)

        # Port
        options_layout.addWidget(QLabel('Port:'), 21, 0)
        self.port = QSpinBox()
        self.port.setRange(1, 65535)
        self.port.setValue(5120)
        options_layout.addWidget(self.port, 21, 1)

        # NWSync URL
        options_layout.addWidget(QLabel('NWSync URL:'), 22, 0)
        self.nwsync_url = QLineEdit()
        options_layout.addWidget(self.nwsync_url, 22, 1)
        # NWSync Hash
        options_layout.addWidget(QLabel('NWSync Hash:'), 23, 0)
        self.nwsync_hash = QLineEdit()
        options_layout.addWidget(self.nwsync_hash, 23, 1)
        # NWSync Publish HAKs
        self.nwsync_publish = QCheckBox('NWSync Publish HAKs')
        options_layout.addWidget(self.nwsync_publish, 24, 0, 1, 2)
        # Quiet
        self.quiet = QCheckBox('Quiet Mode')
        options_layout.addWidget(self.quiet, 25, 0, 1, 2)
        # Interactive
        self.interactive = QCheckBox('Interactive Mode')
        options_layout.addWidget(self.interactive, 26, 0, 1, 2)

        options_group.setLayout(options_layout)
        layout.addWidget(options_group)

        # Paths
        path_group = QGroupBox('Paths')
        path_layout = QGridLayout()
        path_layout.addWidget(QLabel('User Directory:'), 0, 0)
        self.user_dir = QLineEdit()
        path_layout.addWidget(self.user_dir, 0, 1)
        self.user_dir_btn = QPushButton('Browse')
        self.user_dir_btn.clicked.connect(self.browse_user_dir)
        path_layout.addWidget(self.user_dir_btn, 0, 2)

        path_layout.addWidget(QLabel('nwserver-linux Path:'), 1, 0)
        self.nwserver_path = QLineEdit()
        path_layout.addWidget(self.nwserver_path, 1, 1)
        self.nwserver_path_btn = QPushButton('Browse')
        self.nwserver_path_btn.clicked.connect(self.browse_nwserver_path)
        path_layout.addWidget(self.nwserver_path_btn, 1, 2)
        path_group.setLayout(path_layout)
        layout.addWidget(path_group)

        # Start button
        self.start_btn = QPushButton('Start Server')
        self.start_btn.clicked.connect(self.start_server)
        layout.addWidget(self.start_btn)

        # Output (make resizable)
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(options_group)
        splitter.addWidget(path_group)
        splitter.addWidget(self.start_btn)
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        splitter.addWidget(self.output)
        layout.addWidget(splitter)
        self.setLayout(layout)
        
        # Connect signals to auto-save config when values change
        self.server_name.textChanged.connect(self.save_config)
        self.difficulty.currentIndexChanged.connect(self.save_config)
        self.autosave.valueChanged.connect(self.save_config)
        self.level_min.valueChanged.connect(self.save_config)
        self.level_max.valueChanged.connect(self.save_config)
        self.max_players.valueChanged.connect(self.save_config)
        self.local_chars.toggled.connect(self.save_config)
        self.legal_chars.toggled.connect(self.save_config)
        self.item_restrict.toggled.connect(self.save_config)
        self.one_party.toggled.connect(self.save_config)
        self.reload_empty.toggled.connect(self.save_config)
        self.module_path.textChanged.connect(self.save_config)
        self.game_type.currentIndexChanged.connect(self.save_config)
        self.pvp_type.currentIndexChanged.connect(self.save_config)
        self.player_password.textChanged.connect(self.save_config)
        self.dm_password.textChanged.connect(self.save_config)
        self.admin_password.textChanged.connect(self.save_config)
        self.server_message.textChanged.connect(self.save_config)
        self.save_game.textChanged.connect(self.save_config)
        self.slot_number.valueChanged.connect(self.save_config)
        self.public_server.toggled.connect(self.save_config)
        self.port.valueChanged.connect(self.save_config)
        self.user_dir.textChanged.connect(self.save_config)
        self.nwserver_path.textChanged.connect(self.save_config)
        self.nwsync_url.textChanged.connect(self.save_config)
        self.nwsync_hash.textChanged.connect(self.save_config)
        self.nwsync_publish.toggled.connect(self.save_config)
        self.quiet.toggled.connect(self.save_config)
        self.interactive.toggled.connect(self.save_config)

    def browse_user_dir(self):
        dir_ = QFileDialog.getExistingDirectory(self, 'Select User Directory')
        if dir_:
            self.user_dir.setText(dir_)

    def browse_nwserver_path(self):
        file_, _ = QFileDialog.getOpenFileName(self, 'Select nwserver-linux Binary')
        if file_:
            self.nwserver_path.setText(file_)

    def browse_module_path(self):
        file_, _ = QFileDialog.getOpenFileName(self, 'Select Module File')
        if file_:
            self.module_path.setText(file_)

    def browse_save_game(self):
        file_, _ = QFileDialog.getSaveFileName(self, 'Select Save Game File')
        if file_:
            self.save_game.setText(file_)

    def load_config(self):
        config = configparser.ConfigParser()
        if os.path.exists(self.config_file):
            config.read(self.config_file)
            s = config['server']
            self.server_name.setText(s.get('server_name', 'Server'))
            self.difficulty.setCurrentIndex(int(s.get('difficulty', 0)))
            self.autosave.setValue(int(s.get('autosave', 0)))
            self.level_min.setValue(int(s.get('level_min', 1)))
            self.level_max.setValue(int(s.get('level_max', 40)))
            self.max_players.setValue(int(s.get('max_players', 6)))
            self.local_chars.setChecked(s.get('local_chars', '1') == '1')
            self.legal_chars.setChecked(s.get('legal_chars', '0') == '1')
            self.item_restrict.setChecked(s.get('item_restrict', '0') == '1')
            self.one_party.setChecked(s.get('one_party', '1') == '1')
            self.reload_empty.setChecked(s.get('reload_empty', '0') == '1')
            self.module_path.setText(s.get('module_path', ''))
            self.game_type.setCurrentIndex(int(s.get('game_type', 0)))
            self.pvp_type.setCurrentIndex(int(s.get('pvp_type', 0)))
            self.player_password.setText(s.get('player_password', ''))
            self.dm_password.setText(s.get('dm_password', ''))
            self.admin_password.setText(s.get('admin_password', ''))
            self.server_message.setText(s.get('server_message', ''))
            self.save_game.setText(s.get('save_game', ''))
            self.slot_number.setValue(int(s.get('slot_number', 0)))
            self.public_server.setChecked(s.get('public_server', '1') == '1')
            self.port.setValue(int(s.get('port', 5120)))
            self.user_dir.setText(s.get('user_dir', ''))
            self.nwserver_path.setText(s.get('nwserver_path', ''))
            self.nwsync_url.setText(s.get('nwsync_url', ''))
            self.nwsync_hash.setText(s.get('nwsync_hash', ''))
            self.nwsync_publish.setChecked(s.get('nwsync_publish', '0') == '1')
            self.quiet.setChecked(s.get('quiet', '0') == '1')
            self.interactive.setChecked(s.get('interactive', '0') == '1')

    def save_config(self):
        config = configparser.ConfigParser()
        config['server'] = {
            'server_name': self.server_name.text(),
            'difficulty': str(self.difficulty.currentIndex()),
            'autosave': str(self.autosave.value()),
            'level_min': str(self.level_min.value()),
            'level_max': str(self.level_max.value()),
            'max_players': str(self.max_players.value()),
            'local_chars': '1' if self.local_chars.isChecked() else '0',
            'legal_chars': '1' if self.legal_chars.isChecked() else '0',
            'item_restrict': '1' if self.item_restrict.isChecked() else '0',
            'one_party': '1' if self.one_party.isChecked() else '0',
            'reload_empty': '1' if self.reload_empty.isChecked() else '0',
            'module_path': self.module_path.text(),
            'game_type': str(self.game_type.currentIndex()),
            'pvp_type': str(self.pvp_type.currentIndex()),
            'player_password': self.player_password.text(),
            'dm_password': self.dm_password.text(),
            'admin_password': self.admin_password.text(),
            'server_message': self.server_message.text(),
            'save_game': self.save_game.text(),
            'slot_number': str(self.slot_number.value()),
            'public_server': '1' if self.public_server.isChecked() else '0',
            'port': str(self.port.value()),
            'user_dir': self.user_dir.text(),
            'nwserver_path': self.nwserver_path.text(),
            'nwsync_url': self.nwsync_url.text(),
            'nwsync_hash': self.nwsync_hash.text(),
            'nwsync_publish': '1' if self.nwsync_publish.isChecked() else '0',
            'quiet': '1' if self.quiet.isChecked() else '0',
            'interactive': '1' if self.interactive.isChecked() else '0',
        }
        with open(self.config_file, 'w') as configfile:
            config.write(configfile)

    def start_server(self):
        if self.process:
            self.output.append('Server already running.')
            return
        cmd = [self.nwserver_path.text()]        # Use -userdirectory if user directory is set (should be early in command)
        if self.user_dir.text():
            user_dir = self.user_dir.text()
            
            self.output.append(f"Using user directory: {user_dir}")
            
            # Create user directory if it doesn't exist
            try:
                os.makedirs(user_dir, exist_ok=True)
                self.output.append(f"User directory created/verified: {user_dir}")
            except Exception as e:
                self.output.append(f"Error creating user directory: {str(e)}")
                return
            cmd += ['-userdirectory', user_dir]
        
        # Map difficulty dropdown to correct values (1-4)
        difficulty_map = [1, 2, 3, 4]
        cmd += ['-difficulty', str(difficulty_map[self.difficulty.currentIndex()])]
        cmd += ['-autosaveinterval', str(self.autosave.value())]
        cmd += ['-minlevel', str(self.level_min.value())]
        cmd += ['-maxlevel', str(self.level_max.value())]
        cmd += ['-maxclients', str(self.max_players.value())]
        
        # Use -servervault for local/server characters
        if self.local_chars.isChecked():
            cmd += ['-servervault', '0']
        else:
            cmd += ['-servervault', '1']
            
        # Boolean flags as 0/1
        cmd += ['-elc', '1' if self.legal_chars.isChecked() else '0']
        cmd += ['-ilr', '1' if self.item_restrict.isChecked() else '0']
        cmd += ['-oneparty', '1' if self.one_party.isChecked() else '0']
        cmd += ['-reloadwhenempty', '1' if self.reload_empty.isChecked() else '0']
        cmd += ['-pauseandplay', '1']  # Allow players to pause        # Pass only the module name (no path, no .mod)
        if self.module_path.text():
            module_name = os.path.splitext(os.path.basename(self.module_path.text()))[0]
              # Check nwn.ini in user directory for correct paths
            module_found = False
            if self.user_dir.text():
                nwn_ini_path = os.path.join(self.user_dir.text(), 'nwn.ini')
                if os.path.exists(nwn_ini_path):
                    try:
                        import configparser
                        ini_config = configparser.ConfigParser()
                        ini_config.read(nwn_ini_path)
                        
                        if 'Alias' in ini_config and 'MODULES' in ini_config['Alias']:
                            modules_path = ini_config['Alias']['MODULES']
                            
                            # Handle different path formats
                            if modules_path.startswith('C:'):
                                # Windows path - convert to WSL path
                                modules_path = modules_path.replace('C:', '/mnt/c').replace('\\', '/')
                            # If it's already a Linux path (starts with /), use as-is
                            # If it's a relative path, make it relative to user directory
                            elif not modules_path.startswith('/'):
                                modules_path = os.path.join(self.user_dir.text(), modules_path)
                            
                            module_file_path = os.path.join(modules_path, f'{module_name}.mod')
                            if os.path.exists(module_file_path):
                                self.output.append(f"Found module at: {module_file_path} (from nwn.ini)")
                                module_found = True
                            else:
                                self.output.append(f"Module '{module_name}.mod' not found at: {module_file_path}")
                                # Also show what the original nwn.ini path was
                                self.output.append(f"  (nwn.ini MODULES path: {ini_config['Alias']['MODULES']})")
                        else:
                            self.output.append("No MODULES path found in nwn.ini")
                    except Exception as e:
                        self.output.append(f"Error reading nwn.ini: {str(e)}")
                else:
                    self.output.append(f"nwn.ini not found at: {nwn_ini_path}")
            
            # Fallback checks if nwn.ini method didn't work
            if not module_found:
                user_mod_path = os.path.join(self.user_dir.text(), 'modules', f'{module_name}.mod') if self.user_dir.text() else None
                game_mod_path = os.path.join(os.path.dirname(self.nwserver_path.text()), '..', '..', 'modules', f'{module_name}.mod') if self.nwserver_path.text() else None
                
                if user_mod_path and os.path.exists(user_mod_path):
                    self.output.append(f"Found module at: {user_mod_path}")
                    module_found = True
                elif game_mod_path and os.path.exists(game_mod_path):
                    self.output.append(f"Found module at: {game_mod_path}")
                    module_found = True
                else:
                    self.output.append(f"Warning: Module '{module_name}.mod' not found in expected locations:")
                    if user_mod_path:
                        self.output.append(f"  - {user_mod_path}")
                    if game_mod_path:
                        self.output.append(f"  - {game_mod_path}")
            
            cmd += ['-module', module_name]
            
        # Game type as int (1-based, not 0-based)
        if self.game_type.currentIndex() >= 0:
            cmd += ['-gametype', str(self.game_type.currentIndex() + 1)]
            
        # PvP as int (None=0, Party=1, Full=2)
        if self.pvp_type.currentIndex() >= 0:
            cmd += ['-pvp', str(self.pvp_type.currentIndex())]
            
        # Passwords
        if self.player_password.text():
            cmd += ['-playerpassword', self.player_password.text()]
        if self.dm_password.text():
            cmd += ['-dmpassword', self.dm_password.text()]
        if self.admin_password.text():
            cmd += ['-adminpassword', self.admin_password.text()]
            
        # Server name (not server message)
        if self.server_name.text():
            cmd += ['-servername', self.server_name.text()]
            
        # Load saved game - needs both slot and save name
        if self.save_game.text() and self.slot_number.value() >= 0:
            save_name = os.path.splitext(os.path.basename(self.save_game.text()))[0]
            cmd += ['-load', str(self.slot_number.value()), save_name]
            
        cmd += ['-publicserver', '1' if self.public_server.isChecked() else '0']
        
        if self.port.value():
            cmd += ['-port', str(self.port.value())]
            
        # NWSync options
        if self.nwsync_url.text():
            cmd += ['-nwsyncurl', self.nwsync_url.text()]
        if self.nwsync_hash.text():
            cmd += ['-nwsynchash', self.nwsync_hash.text()]
        if self.nwsync_publish.isChecked():
            cmd.append('-nwsyncpublishhaks')
            
        # Mode flags (these are standalone flags, not parameters)
        if self.quiet.isChecked():
            cmd.append('-quiet')
        if self.interactive.isChecked():
            cmd.append('-interactive')
              # Set working directory to the directory containing nwserver-linux
        nwserver_dir = os.path.dirname(self.nwserver_path.text()) if self.nwserver_path.text() else None
        workdir = nwserver_dir
        
        self.output.append(f'Running: {" ".join(cmd)}')
        try:
            self.process = subprocess.Popen(cmd, cwd=workdir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True)
            self.output.append('Server started. Monitoring output...')
            # Don't block the GUI - start a timer to read output periodically
            self.timer = QTimer()
            self.timer.timeout.connect(self.read_output)
            self.timer.start(100)  # Check every 100ms
        except Exception as e:
            self.output.append(f'Error: {e}')
            self.process = None

    def read_output(self):
        if not self.process:
            return
        # Non-blocking read to avoid freezing the GUI
        if self.process.poll() is None:  # Process is still running
            try:
                # Read available lines without blocking
                while True:
                    line = self.process.stdout.readline()
                    if not line:
                        break
                    line_text = line.strip()
                    
                    # Highlight important server messages
                    if "Working Directory For Your Resources Is:" in line_text:
                        self.output.append(f">>> {line_text}")
                        # Extract and verify the path
                        if ":" in line_text:
                            reported_path = line_text.split(":", 1)[1].strip()
                            expected_path = self.user_dir.text()
                            if reported_path != expected_path:
                                self.output.append(f">>> WARNING: Server using different path than expected!")
                                self.output.append(f">>> Expected: {expected_path}")
                                self.output.append(f">>> Actual: {reported_path}")
                    elif "Working Directory For Game Install Is:" in line_text:
                        self.output.append(f">>> {line_text}")
                    else:
                        self.output.append(line_text)
            except:
                pass
        else:
            # Process has finished
            self.timer.stop()
            self.output.append('Server process ended.')
            self.process = None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = NWServerFrontend()
    win.show()
    sys.exit(app.exec_())
