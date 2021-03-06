import os
import pathlib
import subprocess

from gs_extensions.exceptions import GnomeShellNotInstalledError
from gs_extensions.gnome_shell_extension_wrapper import GnomeShellExtensionWrapper
from gs_extensions.exceptions import NoExtensionVersionForGnomeShell, ExtensionNotFoundInHub


class GnomeShellWrapper:
    def __init__(self):
        self.extensions_path = os.path.join(str(pathlib.Path.home()), '.local', 'share', 'gnome-shell', 'extensions')
        self.__major_version = None
        self.__middle_version = None
        self.__minor_version = None
        self.__set_version()
        self.__installed_extensions = self.__get_installed_extensions()

    def __repr__(self):
        return 'Gnome Shell: version {}'.format(self.get_full_version)

    def get_installed_extensions(self):
        return self.__installed_extensions

    def add_installed_extension(self, extension):
        self.__installed_extensions.append(extension)
        return self.__installed_extensions

    @property
    def get_short_version(self):
        return '.'.join([self.__major_version, self.__middle_version])

    @property
    def get_full_version(self):
        if self.__minor_version is None:
            return self.get_short_version
        return '.'.join([self.get_short_version, self.__minor_version])

    def create_extensions_folder_if_not_exists(self):
        if not os.path.exists(self.extensions_path):
            os.mkdir(self.extensions_path)

    def get_extensions_from_file(self, filename):
        with open(filename) as file_with_extensions:
            extensions_to_install = []
            for uuid in file_with_extensions.readlines():
                clear_uuid = uuid.replace('\n', '')
                extensions_to_install.append(GnomeShellExtensionWrapper.from_uuid(clear_uuid, self))
            return extensions_to_install

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

    def __get_installed_extensions(self):
        list_of_extension_folders = os.listdir(self.extensions_path)
        gnome_shell_extensions_list = []
        for uuid in list_of_extension_folders:
            try:
                extension = GnomeShellExtensionWrapper.from_uuid(uuid=uuid, gnome_shell=self)
                gnome_shell_extensions_list.append(extension)
            except NoExtensionVersionForGnomeShell:
                pass
        return gnome_shell_extensions_list
