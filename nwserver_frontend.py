import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QComboBox, QSpinBox, QCheckBox, QFileDialog, QTextEdit, QGroupBox, QGridLayout
)
from PyQt5.QtCore import Qt

class NWServerFrontend(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('NWServer-Linux Frontend')
        self.init_ui()
        self.process = None

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

        # Checkboxes
        self.local_chars = QCheckBox('Local Characters Allowed')
        self.legal_chars = QCheckBox('Enforce Legal Characters')
        self.item_restrict = QCheckBox('Item Level Restrictions')
        self.one_party = QCheckBox('Only One Party')
        self.pause_enabled = QCheckBox('Player Pause Enabled')
        self.reload_empty = QCheckBox('Reload When Empty')
        self.local_chars.setChecked(True)
        self.one_party.setChecked(True)
        self.pause_enabled.setChecked(True)
        options_layout.addWidget(self.local_chars, 5, 0, 1, 2)
        options_layout.addWidget(self.legal_chars, 6, 0, 1, 2)
        options_layout.addWidget(self.item_restrict, 7, 0, 1, 2)
        options_layout.addWidget(self.one_party, 8, 0, 1, 2)
        options_layout.addWidget(self.pause_enabled, 9, 0, 1, 2)
        options_layout.addWidget(self.reload_empty, 10, 0, 1, 2)

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

        # Output
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.setLayout(layout)

    def browse_user_dir(self):
        dir_ = QFileDialog.getExistingDirectory(self, 'Select User Directory')
        if dir_:
            self.user_dir.setText(dir_)

    def browse_nwserver_path(self):
        file_, _ = QFileDialog.getOpenFileName(self, 'Select nwserver-linux Binary')
        if file_:
            self.nwserver_path.setText(file_)

    def start_server(self):
        if self.process:
            self.output.append('Server already running.')
            return
        cmd = [self.nwserver_path.text()]
        # Example: add options as command-line args
        if self.server_name.text():
            cmd += ['-servername', self.server_name.text()]
        cmd += ['-difficulty', str(self.difficulty.currentIndex())]
        cmd += ['-autosaveinterval', str(self.autosave.value())]
        cmd += ['-minlevel', str(self.level_min.value())]
        cmd += ['-maxlevel', str(self.level_max.value())]
        cmd += ['-maxclients', str(self.max_players.value())]
        if self.local_chars.isChecked():
            cmd.append('-localchars')
        if self.legal_chars.isChecked():
            cmd.append('-legalchars')
        if self.item_restrict.isChecked():
            cmd.append('-itemlevelrestrictions')
        if self.one_party.isChecked():
            cmd.append('-oneparty')
        if self.pause_enabled.isChecked():
            cmd.append('-playerpause')
        if self.reload_empty.isChecked():
            cmd.append('-reloadwhenempty')
        # Set user dir as working directory
        workdir = self.user_dir.text() if self.user_dir.text() else None
        self.output.append(f'Running: {" ".join(cmd)}')
        try:
            self.process = subprocess.Popen(cmd, cwd=workdir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            self.output.append('Server started. Output:')
            self.read_output()
        except Exception as e:
            self.output.append(f'Error: {e}')
            self.process = None

    def read_output(self):
        if not self.process:
            return
        while True:
            line = self.process.stdout.readline()
            if not line:
                break
            self.output.append(line)
        self.process = None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = NWServerFrontend()
    win.show()
    sys.exit(app.exec_())
