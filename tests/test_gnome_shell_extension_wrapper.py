from unittest import TestCase
from unittest.mock import patch, mock_open

from gs_extensions.exceptions import NoExtensionVersionForGnomeShell
from gs_extensions.gnome_shell_extension_wrapper import GnomeShellExtensionWrapper


class ResponseMock:
    def __init__(self, response, status):
        self.response = response
        self.status_code = status

    def json(self):
        return self.response


class TestGnomeShellExtensionWrapper(TestCase):
    def setUp(self):
        self.response_json_with_long_version = {
            "shell_version_map": {"3.28.3": {"pk": 8419, "version": 30}}, "pk": 517, "uuid": "caffeine@patapon.info"
        }
        self.response_json_with_short_version = {
            "shell_version_map": {"3.28": {"pk": 8419, "version": 30}}, "pk": 517, "uuid": "caffeine@patapon.info"
        }
        self.response_status_code_ok = 200
        self.response_status_code_not_found = 404

    @patch('gs_extensions.gnome_shell_extension_wrapper.requests.get')
    @patch('gs_extensions.gnome_shell_wrapper.GnomeShellWrapper')
    def test_from_uuid_with_long_gs_version(self, gnome_shell, requests_get):
        gnome_shell.get_full_version.return_value = '3.28.3'
        requests_get.return_value = ResponseMock(self.response_json_with_long_version, self.response_status_code_ok)
        gnome_shell_extension = GnomeShellExtensionWrapper.from_uuid(uuid='caffeine@patapon.info',
                                                                     gnome_shell=gnome_shell)
        self.assertEqual(gnome_shell_extension.pk, 517)
        self.assertEqual(gnome_shell_extension.uuid, 'caffeine@patapon.info')
        self.assertEqual(gnome_shell_extension.version, 30)

    @patch('gs_extensions.gnome_shell_extension_wrapper.requests.get')
    @patch('gs_extensions.gnome_shell_wrapper.GnomeShellWrapper')
    def test_from_pk_with_long_gs_version(self, gnome_shell, requests_get):
        gnome_shell.get_full_version.return_value = '3.28.3'
        requests_get.return_value = ResponseMock(self.response_json_with_long_version, self.response_status_code_ok)
        gnome_shell_extension = GnomeShellExtensionWrapper.from_pk(pk=517, gnome_shell=gnome_shell)
        self.assertEqual(gnome_shell_extension.pk, 517)
        self.assertEqual(gnome_shell_extension.uuid, 'caffeine@patapon.info')
        self.assertEqual(gnome_shell_extension.version, 30)

    @patch('gs_extensions.gnome_shell_extension_wrapper.requests.get')
    @patch('gs_extensions.gnome_shell_wrapper.GnomeShellWrapper')
    def test_from_uuid_with_short_gs_version(self, gnome_shell, requests_get):
        gnome_shell.get_full_version.return_value = '3.28'
        requests_get.return_value = ResponseMock(self.response_json_with_short_version, self.response_status_code_ok)
        gnome_shell_extension = GnomeShellExtensionWrapper.from_uuid(uuid='caffeine@patapon.info',
                                                                     gnome_shell=gnome_shell)
        self.assertEqual(gnome_shell_extension.pk, 517)
        self.assertEqual(gnome_shell_extension.uuid, 'caffeine@patapon.info')
        self.assertEqual(gnome_shell_extension.version, 30)

    @patch('gs_extensions.gnome_shell_extension_wrapper.requests.get')
    @patch('gs_extensions.gnome_shell_wrapper.GnomeShellWrapper')
    def test_from_pk_with_short_gs_version(self, gnome_shell, requests_get):
        gnome_shell.get_full_version.return_value = '3.28'
        requests_get.return_value = ResponseMock(self.response_json_with_short_version, self.response_status_code_ok)
        gnome_shell_extension = GnomeShellExtensionWrapper.from_pk(pk=517, gnome_shell=gnome_shell)
        self.assertEqual(gnome_shell_extension.pk, 517)
        self.assertEqual(gnome_shell_extension.uuid, 'caffeine@patapon.info')
        self.assertEqual(gnome_shell_extension.version, 30)

    @patch('gs_extensions.gnome_shell_extension_wrapper.requests.get')
    @patch('gs_extensions.gnome_shell_wrapper.GnomeShellWrapper')
    def test_from_uuid_fails_with_exception(self, gnome_shell, requests_get):
        gnome_shell.get_full_version.return_value = '3.30'
        requests_get.return_value = ResponseMock(self.response_json_with_short_version, self.response_status_code_ok)
        with self.assertRaises(NoExtensionVersionForGnomeShell):
            GnomeShellExtensionWrapper.from_uuid(uuid='caffeine@patapon.info', gnome_shell=gnome_shell)

    @patch('gs_extensions.gnome_shell_extension_wrapper.requests.get')
    @patch('gs_extensions.gnome_shell_wrapper.GnomeShellWrapper')
    def test_from_pk_fails_with_exception(self, gnome_shell, requests_get):
        gnome_shell.get_full_version.return_value = '3.30'
        requests_get.return_value = ResponseMock(self.response_json_with_short_version, self.response_status_code_ok)
        with self.assertRaises(NoExtensionVersionForGnomeShell):
            GnomeShellExtensionWrapper.from_pk(pk=517, gnome_shell=gnome_shell)
