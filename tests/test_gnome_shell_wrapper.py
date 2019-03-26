import unittest
from unittest.mock import patch

from gs_extensions.exceptions import GnomeShellNotInstalledError
from gs_extensions.gnome_shell_wrapper import GnomeShellWrapper


def raise_file_not_found_exception(*args, **kwargs):
    raise GnomeShellNotInstalledError()


class TestGnomeShellWrapper(unittest.TestCase):
    @patch('gs_extensions.gnome_shell_wrapper.subprocess.check_output', return_value='GNOME Shell 3.28.3'.encode())
    def test_full_version(self, _):
        gs_wrapper = GnomeShellWrapper()
        self.assertEqual(gs_wrapper.get_full_version, '3.28.3')

    @patch('gs_extensions.gnome_shell_wrapper.subprocess.check_output', return_value='GNOME Shell 3.28.3'.encode())
    def test_short_version(self, _):
        gs_wrapper = GnomeShellWrapper()
        self.assertEqual(gs_wrapper.get_short_version, '3.28')

    @patch('gs_extensions.gnome_shell_wrapper.subprocess.check_output', return_value='GNOME Shell 3.28'.encode())
    def test_full_version_for_short_gnome_version(self, _):
        gs_wrapper = GnomeShellWrapper()
        self.assertEqual(gs_wrapper.get_full_version, '3.28')

    @patch('gs_extensions.gnome_shell_wrapper.subprocess.check_output', return_value='GNOME Shell 3.28'.encode())
    def test_short_version_for_short_gnome_version(self, _):
        gs_wrapper = GnomeShellWrapper()
        self.assertEqual(gs_wrapper.get_short_version, '3.28')

    @patch('gs_extensions.gnome_shell_wrapper.subprocess.check_output',
           **{'return_value.decode.side_effect': GnomeShellNotInstalledError()})
    def test_run_without_gnome_shell_installed(self, _):
        with self.assertRaises(GnomeShellNotInstalledError):
            gs_wrapper = GnomeShellWrapper()

    @patch('gs_extensions.gnome_shell_wrapper.pathlib.Path.home', return_value='/home/user')
    @patch('gs_extensions.gnome_shell_wrapper.subprocess.check_output', side_effects='GNOME Shell 3.28'.encode())
    def test_extensions_path(self, check_output_, home_):
        gs_wrapper = GnomeShellWrapper()
        self.assertEqual(gs_wrapper.extensions_path, '/home/user/.local/share/gnome-shell/extensions')

    @patch('gs_extensions.gnome_shell_wrapper.GnomeShellExtensionWrapper.from_uuid', return_value='yes')
    @patch('gs_extensions.gnome_shell_wrapper.os.listdir', return_value=['one', 'two', 'tree'])
    @patch('gs_extensions.gnome_shell_wrapper.pathlib.Path.home', return_value='/home/user')
    @patch('gs_extensions.gnome_shell_wrapper.subprocess.check_output', side_effects='GNOME Shell 3.28'.encode())
    def test_installed_extensions(self, check_output_, home_, os_, gse_wrapper):
        gs_wrapper = GnomeShellWrapper()
        self.assertEqual(gs_wrapper.extensions_path, '/home/user/.local/share/gnome-shell/extensions')
        self.assertEqual(gs_wrapper.get_installed_extensions(), ['yes', 'yes', 'yes', ])
