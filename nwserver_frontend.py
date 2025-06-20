import sys
import subprocess
import os
import configparser
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QComboBox, QSpinBox, QCheckBox, QFileDialog, QTextEdit, QGroupBox, QGridLayout, QSplitter, QScrollArea
)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
import threading
import queue

class NWServerFrontend(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('NWServer-Linux Frontend')
        self.init_ui()
        self.process = None
        self.config_file = os.path.join(os.path.dirname(__file__), 'nwserver_frontend.ini')
        self.output_queue = queue.Queue()
        self.load_config()
        
    def closeEvent(self, event):
        """Save configuration when the application is closed"""
        self.save_config()
        event.accept()

    def init_ui(self):
        # Create main horizontal splitter for side-by-side layout
        main_splitter = QSplitter(Qt.Horizontal)
        
        # Left panel for configuration
        config_widget = QWidget()
        config_layout = QVBoxLayout(config_widget)
        
        # Basic Server Settings
        basic_group = QGroupBox('Basic Settings')
        basic_layout = QGridLayout()
        
        basic_layout.addWidget(QLabel('Server Name:'), 0, 0)
        self.server_name = QLineEdit('Server')
        basic_layout.addWidget(self.server_name, 0, 1)
        
        basic_layout.addWidget(QLabel('Difficulty:'), 1, 0)
        self.difficulty = QComboBox()
        self.difficulty.addItems(['Easy', 'Normal', 'Hardcore', 'Very Difficult'])
        basic_layout.addWidget(self.difficulty, 1, 1)
        
        basic_layout.addWidget(QLabel('Max Players:'), 2, 0)
        self.max_players = QSpinBox()
        self.max_players.setRange(1, 255)
        self.max_players.setValue(6)
        basic_layout.addWidget(self.max_players, 2, 1)
        
        basic_layout.addWidget(QLabel('Port:'), 3, 0)
        self.port = QSpinBox()
        self.port.setRange(1, 65535)
        self.port.setValue(5120)
        basic_layout.addWidget(self.port, 3, 1)
        
        basic_group.setLayout(basic_layout)
        
        # Game Settings
        game_group = QGroupBox('Game Settings')
        game_layout = QGridLayout()
        
        game_layout.addWidget(QLabel('Levels:'), 0, 0)
        self.level_min = QSpinBox()
        self.level_min.setRange(1, 40)
        self.level_max = QSpinBox()
        self.level_max.setRange(1, 40)
        self.level_max.setValue(40)
        level_layout = QHBoxLayout()
        level_layout.addWidget(self.level_min)
        level_layout.addWidget(QLabel('to'))
        level_layout.addWidget(self.level_max)
        game_layout.addLayout(level_layout, 0, 1)
        
        game_layout.addWidget(QLabel('Game Type:'), 1, 0)
        self.game_type = QComboBox()
        self.game_type.addItems(['Action', 'Story', 'Custom'])
        game_layout.addWidget(self.game_type, 1, 1)
        
        game_layout.addWidget(QLabel('Player vs. Player:'), 2, 0)
        self.pvp_type = QComboBox()
        self.pvp_type.addItems(['None', 'Party', 'Full'])
        game_layout.addWidget(self.pvp_type, 2, 1)
        
        game_layout.addWidget(QLabel('Autosave (min):'), 3, 0)
        self.autosave = QSpinBox()
        self.autosave.setRange(0, 120)
        game_layout.addWidget(self.autosave, 3, 1)
        
        game_group.setLayout(game_layout)
        
        # Options
        options_group = QGroupBox('Options')
        options_layout = QGridLayout()
        
        self.local_chars = QCheckBox('Local Characters Allowed')
        self.legal_chars = QCheckBox('Enforce Legal Characters')
        self.item_restrict = QCheckBox('Item Level Restrictions')
        self.one_party = QCheckBox('Only One Party')
        self.reload_empty = QCheckBox('Reload When Empty')
        self.public_server = QCheckBox('Post Game To Internet')
        self.local_chars.setChecked(True)
        self.one_party.setChecked(True)
        self.public_server.setChecked(True)
        
        options_layout.addWidget(self.local_chars, 0, 0)
        options_layout.addWidget(self.legal_chars, 0, 1)
        options_layout.addWidget(self.item_restrict, 1, 0)
        options_layout.addWidget(self.one_party, 1, 1)
        options_layout.addWidget(self.reload_empty, 2, 0)
        options_layout.addWidget(self.public_server, 2, 1)
        
        options_group.setLayout(options_layout)
        
        # Paths
        path_group = QGroupBox('Paths')
        path_layout = QGridLayout()
        
        path_layout.addWidget(QLabel('Module Name:'), 0, 0)
        self.module_name = QLineEdit()
        self.module_name.setPlaceholderText('e.g. mymodule (without .mod extension)')
        path_layout.addWidget(self.module_name, 0, 1, 1, 2)
        
        path_layout.addWidget(QLabel('User Directory:'), 1, 0)
        self.user_dir = QLineEdit()
        path_layout.addWidget(self.user_dir, 1, 1)
        self.user_dir_btn = QPushButton('Browse')
        self.user_dir_btn.clicked.connect(self.browse_user_dir)
        path_layout.addWidget(self.user_dir_btn, 1, 2)
        
        path_layout.addWidget(QLabel('nwserver-linux Path:'), 2, 0)
        self.nwserver_path = QLineEdit()
        path_layout.addWidget(self.nwserver_path, 2, 1)
        self.nwserver_path_btn = QPushButton('Browse')
        self.nwserver_path_btn.clicked.connect(self.browse_nwserver_path)
        path_layout.addWidget(self.nwserver_path_btn, 2, 2)
        
        path_group.setLayout(path_layout)
        
        # Advanced Settings (collapsible or separate tab)
        advanced_group = QGroupBox('Advanced Settings')
        advanced_layout = QGridLayout()
        
        advanced_layout.addWidget(QLabel('Player Password:'), 0, 0)
        self.player_password = QLineEdit()
        advanced_layout.addWidget(self.player_password, 0, 1)
        
        advanced_layout.addWidget(QLabel('DM Password:'), 1, 0)
        self.dm_password = QLineEdit()
        advanced_layout.addWidget(self.dm_password, 1, 1)
        
        advanced_layout.addWidget(QLabel('Server Admin Password:'), 2, 0)
        self.admin_password = QLineEdit()
        advanced_layout.addWidget(self.admin_password, 2, 1)
        
        advanced_layout.addWidget(QLabel('Server Message:'), 3, 0)
        self.server_message = QLineEdit()
        advanced_layout.addWidget(self.server_message, 3, 1)
        
        advanced_layout.addWidget(QLabel('Save Game:'), 4, 0)
        self.save_game = QLineEdit()
        advanced_layout.addWidget(self.save_game, 4, 1)
        self.save_game_btn = QPushButton('Browse')
        self.save_game_btn.clicked.connect(self.browse_save_game)
        advanced_layout.addWidget(self.save_game_btn, 4, 2)
        
        advanced_layout.addWidget(QLabel('Slot Number:'), 5, 0)
        self.slot_number = QSpinBox()
        self.slot_number.setRange(0, 99)
        advanced_layout.addWidget(self.slot_number, 5, 1)
        
        advanced_layout.addWidget(QLabel('NWSync URL:'), 6, 0)
        self.nwsync_url = QLineEdit()
        advanced_layout.addWidget(self.nwsync_url, 6, 1)
        
        advanced_layout.addWidget(QLabel('NWSync Hash:'), 7, 0)
        self.nwsync_hash = QLineEdit()
        advanced_layout.addWidget(self.nwsync_hash, 7, 1)
        
        self.nwsync_publish = QCheckBox('NWSync Publish HAKs')
        advanced_layout.addWidget(self.nwsync_publish, 8, 0, 1, 2)
        
        self.quiet = QCheckBox('Quiet Mode')
        advanced_layout.addWidget(self.quiet, 9, 0)
        
        self.interactive = QCheckBox('Interactive Mode')
        advanced_layout.addWidget(self.interactive, 9, 1)
        
        advanced_group.setLayout(advanced_layout)
        
        # Add all groups to config layout
        config_layout.addWidget(basic_group)
        config_layout.addWidget(game_group)
        config_layout.addWidget(options_group)
        config_layout.addWidget(path_group)
        config_layout.addWidget(advanced_group)
        
        # Start button
        self.start_btn = QPushButton('Start Server')
        self.start_btn.clicked.connect(self.start_server)
        config_layout.addWidget(self.start_btn)
        
        # Add stretch to push everything to top
        config_layout.addStretch()
        
        # Create scroll area for config widget
        scroll_area = QScrollArea()
        scroll_area.setWidget(config_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Right panel for output
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        output_label = QLabel('Server Output:')
        right_layout.addWidget(output_label)
        
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setMinimumHeight(200)
        right_layout.addWidget(self.output)
        
        # Add widgets to main splitter
        main_splitter.addWidget(scroll_area)
        main_splitter.addWidget(right_widget)
        
        # Set initial sizes - config panel gets 60%, output gets 40%
        main_splitter.setSizes([600, 400])
        main_splitter.setStretchFactor(0, 0)  # Config panel doesn't stretch
        main_splitter.setStretchFactor(1, 1)  # Output panel stretches
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(main_splitter)
        self.setLayout(main_layout)
        
        # Set window properties
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)

    def browse_user_dir(self):
        dir_ = QFileDialog.getExistingDirectory(self, 'Select User Directory')
        if dir_:
            self.user_dir.setText(dir_)

    def browse_nwserver_path(self):
        file_, _ = QFileDialog.getOpenFileName(self, 'Select nwserver-linux Binary')
        if file_:
            self.nwserver_path.setText(file_)

    def browse_save_game(self):
        file_, _ = QFileDialog.getSaveFileName(self, 'Select Save Game File')
        if file_:
            self.save_game.setText(file_)

    def load_config(self):
        config = configparser.ConfigParser()
        if os.path.exists(self.config_file):
            try:
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
                self.module_name.setText(s.get('module_name', ''))
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
            except Exception as e:
                print(f"Error loading config: {e}")
                # If config is corrupted, continue with defaults

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
            'module_name': self.module_name.text(),
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
        
        cmd = [self.nwserver_path.text()]
          # Use -userdirectory if user directory is set (should be early in command)
        if self.user_dir.text():
            user_dir = self.user_dir.text()
            
            # Ensure we have an absolute path
            if not os.path.isabs(user_dir):
                user_dir = os.path.abspath(user_dir)
                self.output.append(f"Converting to absolute path: {user_dir}")
            
            self.output.append(f"Using user directory: {user_dir}")
              # Create user directory if it doesn't exist
            try:
                if os.path.exists(user_dir):
                    self.output.append(f"User directory already exists: {user_dir}")
                    # Check if we have write permissions
                    if os.access(user_dir, os.W_OK):
                        self.output.append(f"Write permissions confirmed for: {user_dir}")
                    else:
                        self.output.append(f"WARNING: No write permissions for: {user_dir}")
                else:
                    os.makedirs(user_dir, exist_ok=True)
                    self.output.append(f"User directory created: {user_dir}")
            except PermissionError as e:
                self.output.append(f"Permission error with user directory: {str(e)}")
                self.output.append(f"Make sure you have write access to: {user_dir}")
                return
            except Exception as e:
                self.output.append(f"Error with user directory: {str(e)}")
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
        cmd += ['-pauseandplay', '1']  # Allow players to pause
        
        # Pass the module name directly
        if self.module_name.text():
            cmd += ['-module', self.module_name.text()]
            
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
        
        self.output.append(f'Running: {" ".join(cmd)}')
        if nwserver_dir:
            self.output.append(f'Working directory: {nwserver_dir}')
            
        try:
            # Set working directory to the nwserver-linux directory (usually linux-x86)
            # This is crucial for nwserver to find the game data
            self.process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT, 
                text=True, 
                bufsize=1, 
                universal_newlines=True,
                cwd=nwserver_dir  # Set the working directory
            )
            self.output.append('Server started. Monitoring output...')
            
            # Start a thread to read output without blocking the GUI
            self.output_thread = threading.Thread(target=self.read_output_thread, daemon=True)
            self.output_thread.start()
            
            # Start a timer to check for new output
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_output)
            self.timer.start(100)  # Check every 100ms
        except Exception as e:
            self.output.append(f'Error: {e}')
            self.process = None

    def read_output_thread(self):
        """Thread function to read process output without blocking the GUI"""
        if not self.process:
            return
            
        try:
            for line in iter(self.process.stdout.readline, ''):
                if line:
                    self.output_queue.put(line.strip())
                if self.process.poll() is not None:
                    break
        except Exception as e:
            self.output_queue.put(f"Error reading output: {e}")
        finally:
            self.output_queue.put("__PROCESS_ENDED__")
    
    def update_output(self):
        """Update the output text widget with new lines from the queue"""
        try:
            while True:
                line = self.output_queue.get_nowait()
                if line == "__PROCESS_ENDED__":
                    self.timer.stop()
                    self.output.append('Server process ended.')
                    self.process = None
                    break
                else:
                    self.output.append(line)
        except queue.Empty:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = NWServerFrontend()
    win.show()
    sys.exit(app.exec_())
