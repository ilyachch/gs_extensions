import os
import pathlib
import subprocess

from gs_extensions.exceptions import GnomeShellNotInstalledError
from gs_extensions.gnome_shell_extension_wrapper import GnomeShellExtensionWrapper


class GnomeShellWrapper:
    def __init__(self):
        self.extensions_path = os.path.join(str(pathlib.Path.home()), '.local', 'share', 'gnome-shell', 'extensions')
        self.__major_version = None
        self.__middle_version = None
        self.__minor_version = None
        self.__set_version()

    def __set_version(self):
        try:
            response = subprocess.check_output(['gnome-shell', '--version']).decode()
        except FileNotFoundError:
            raise GnomeShellNotInstalledError()
        clear_response = response.replace('\n', '')
        clear_response = clear_response.replace('GNOME Shell ', '')
        version_parts = clear_response.split('.')
        self.__major_version = self.__get_value_or_none(version_parts, 0)
        self.__middle_version = self.__get_value_or_none(version_parts, 1)
        self.__minor_version = self.__get_value_or_none(version_parts, 2)

    @staticmethod
    def __get_value_or_none(source_list, search_index):
        try:
            return source_list[search_index]
        except IndexError:
            return None

    def get_short_version(self):
        return '.'.join([self.__major_version, self.__middle_version])

    def get_full_version(self):
        if self.__minor_version is None:
            return self.get_short_version()
        return '.'.join([self.get_short_version(), self.__minor_version])

    def get_installed_extensions(self):
        list_of_extensions = os.listdir(self.extensions_path)
        gnome_shell_extensions_list = [GnomeShellExtensionWrapper.from_uuid(uuid=uuid, gnome_shell=self)
                                       for uuid in list_of_extensions]
        return gnome_shell_extensions_list
