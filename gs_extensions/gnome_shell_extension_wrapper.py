import os
import subprocess
import tempfile
import zipfile

import requests

from gs_extensions.exceptions import NoExtensionVersionForGnomeShell, ExtensionNotFoundInHub, ExtensionAlreadyActivated


class GnomeShellExtensionWrapper:
    EXTENSIONS_API_URL = 'https://extensions.gnome.org/ajax/detail/'

    DOWNLOAD_LINK_TPL = 'https://extensions.gnome.org/extension-data/{}.v{}.shell-extension.zip'

    def __init__(self, gnome_shell, pk=None, uuid=None):
        self.gnome_shell = gnome_shell
        self.pk = pk if pk is not None else self.__get_pk_by_uuid(uuid)
        self.uuid = uuid if uuid is not None else self.__get_uuid_by_pk(pk)

        self.version = self.__get_version()

    @classmethod
    def from_uuid(cls, uuid, gnome_shell):
        return cls(
            uuid=uuid,
            gnome_shell=gnome_shell
        )

    @classmethod
    def from_pk(cls, pk, gnome_shell):
        return cls(
            pk=pk,
            gnome_shell=gnome_shell
        )

    @classmethod
    def from_file(cls, filename, gnome_shell):
        with open(filename) as file_with_extensions:
            extensions_to_install = []
            for uuid in file_with_extensions.readlines():
                clear_uuid = uuid.replace('\n', '')
                extensions_to_install.append(cls.from_uuid(clear_uuid, gnome_shell))
            return extensions_to_install

    def __get_uuid_by_pk(self, pk):
        response = requests.get(self.EXTENSIONS_API_URL, {'pk': pk})
        if response.status_code == 404:
            raise ExtensionNotFoundInHub()
        return response.json()['uuid']

    def __get_pk_by_uuid(self, uuid):
        response = requests.get(self.EXTENSIONS_API_URL, {'uuid': uuid})
        if response.status_code == 404:
            raise ExtensionNotFoundInHub()
        return response.json()['pk']

    def __get_version(self):
        response = requests.get(self.EXTENSIONS_API_URL, {'pk': self.pk, 'uuid': self.uuid}).json()
        versions_list = response['shell_version_map']
        q = self.gnome_shell.get_full_version()
        if self.gnome_shell.get_full_version() in versions_list:
            return versions_list[self.gnome_shell.get_full_version()]['version']
        elif self.gnome_shell.get_short_version() in versions_list:
            return versions_list[self.gnome_shell.get_short_version()]['version']
        raise NoExtensionVersionForGnomeShell()

    def install(self):
        self.download()
        self.activate()

    def download(self):
        installed_gnome_shell_extensions = self.gnome_shell.get_installed_extensions()
        installed_gnome_shell_uuid = [gs_extension.uuid for gs_extension in installed_gnome_shell_extensions]
        if self.uuid in installed_gnome_shell_uuid:
            print('{} already downloaded')
        else:
            self.__download_and_unzip()

    def __download_and_unzip(self):
        extension_folder = os.path.join(self.gnome_shell.extensions_path, self.uuid)
        os.mkdir(extension_folder)
        download_link = self.DOWNLOAD_LINK_TPL.format(self.uuid, self.version)
        response = requests.get(download_link)
        temp_file_to_load = tempfile.NamedTemporaryFile(suffix='.zip')
        temp_file_to_load.write(response.content)
        zip_ref = zipfile.ZipFile(temp_file_to_load, 'r')
        zip_ref.extractall(extension_folder)
        zip_ref.close()

    def activate(self):
        try:
            subprocess.call(['gnome-shell-extension-tool', '-e', self.uuid])
        except subprocess.CalledProcessError:
            print('{} already activated'.format(self.uuid))
