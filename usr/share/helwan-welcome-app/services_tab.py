from PyQt5.QtWidgets import (
	QWidget, QVBoxLayout, QGroupBox, QPushButton,
	QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt
import subprocess


def create_services_tab(parent, run_terminal_cmd, _):
	"""
	Create System Services / Quick Fixes tab
	"""

	tab = QWidget()
	layout = QVBoxLayout(tab)
	layout.setAlignment(Qt.AlignTop)

	# =========================
	# System Services Group
	# =========================
	services_group = QGroupBox(_("System Services"))
	services_layout = QVBoxLayout()

	# Restart NetworkManager
	btn_restart_network = QPushButton(_("Restart Network"))
	btn_restart_network.clicked.connect(
		lambda: confirm_and_run(
			parent,
			run_terminal_cmd,
			"pkexec systemctl restart NetworkManager",
			_("Restart Network"),
			_("This will restart NetworkManager. Your connection may drop briefly.")
		)
	)
	services_layout.addWidget(btn_restart_network)

	# Toggle Bluetooth
	btn_toggle_bluetooth = QPushButton(_("Enable / Disable Bluetooth"))
	btn_toggle_bluetooth.clicked.connect(
		lambda: toggle_bluetooth(parent, run_terminal_cmd, _)
	)
	services_layout.addWidget(btn_toggle_bluetooth)

	services_group.setLayout(services_layout)
	layout.addWidget(services_group)

	# =========================
	# Quick Fixes Group
	# =========================
	fixes_group = QGroupBox(_("Quick Fixes"))
	fixes_layout = QVBoxLayout()

	# Rebuild initramfs
	# Rebuild initramfs (Targeting linux-lts specifically)
	btn_initramfs = QPushButton(_("Rebuild LTS Initramfs"))
	btn_initramfs.clicked.connect(
		lambda: confirm_and_run(
			parent,
			run_terminal_cmd,
			"pkexec mkinitcpio -p linux-lts",  # هنا حددنا الـ preset بتاع الـ lts بس
			_("Rebuild Initramfs"),
			_("This will rebuild initramfs specifically for the LTS kernel.")
		)
	)
	fixes_layout.addWidget(btn_initramfs)

	# Update GRUB
	btn_grub = QPushButton(_("Update Bootloader (GRUB)"))
	btn_grub.clicked.connect(
		lambda: confirm_and_run(
			parent,
			run_terminal_cmd,
			"pkexec grub-mkconfig -o /boot/grub/grub.cfg",
			_("Update GRUB"),
			_("This will regenerate GRUB configuration.")
		)
	)
	fixes_layout.addWidget(btn_grub)

	# Fix broken packages
	btn_fix_pkgs = QPushButton(_("Check & Fix Packages"))
	btn_fix_pkgs.clicked.connect(
		lambda: confirm_and_run(
			parent,
			run_terminal_cmd,
			"pkexec pacman -Qkk", 
			_("Check Packages"),
			_("This will check all installed packages for integrity issues.")
		)
	)
	fixes_layout.addWidget(btn_fix_pkgs)

	fixes_group.setLayout(fixes_layout)
	layout.addWidget(fixes_group)

	layout.addStretch(1)
	return tab


# ==================================================
# Helpers
# ==================================================

def confirm_and_run(parent, run_terminal_cmd, command, title, message):
	reply = QMessageBox.question(
		parent,
		title,
		message,
		QMessageBox.Yes | QMessageBox.No,
		QMessageBox.No
	)
	if reply == QMessageBox.Yes:
		run_terminal_cmd(command, title)


def toggle_bluetooth(parent, run_terminal_cmd, _):
	try:
		status = subprocess.getoutput("systemctl is-active bluetooth")
		if status.strip() == "active":
			confirm_and_run(
				parent,
				run_terminal_cmd,
				"pkexec systemctl disable --now bluetooth",
				_("Bluetooth"),
				_("Bluetooth is currently enabled. Disable it?")
			)
		else:
			confirm_and_run(
				parent,
				run_terminal_cmd,
				"pkexec systemctl enable --now bluetooth",
				_("Bluetooth"),
				_("Bluetooth is currently disabled. Enable it?")
			)
	except Exception:
		QMessageBox.critical(
			parent,
			_("Error"),
			_("Unable to detect Bluetooth service status.")
		)
