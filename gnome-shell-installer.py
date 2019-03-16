import argparse
import os
import pathlib
import requests

from bs4 import BeautifulSoup
import json
import tempfile
import zipfile
import subprocess


class App:
    EXTENSION_TPL = 'https://extensions.gnome.org/extension/{}'
    DOWNLOAD_LINK_TPL = 'https://extensions.gnome.org/extension-data/{}.v{}.shell-extension.zip'

    def __init__(self):
        self.parser = argparse.ArgumentParser('CLI tool to install Gnome Shell Extensions.')
        self.args = self.__process_args()
        self.extension_ids = self.args.extension_id
        self.gnome_shell_version = self.args.version
        self.install_path = self.__get_install_path()

    def process(self):
        for extension_id in self.extension_ids:
            self.__process_extension(extension_id)

    def __process_extension(self, extension_id):
        extension_uuid, extension_versions = self.get_data(extension_id)
        extension_version = self.__get_version_of_extension(extension_uuid, extension_versions)

        download_link = self.DOWNLOAD_LINK_TPL.format(extension_uuid, extension_version)
        folder_for_extension = self.__create_folder_for_extension(extension_uuid)
        loaded_extension = self.__load_extensions_archive(download_link)
        self.__unzip_extension_archive_to_extensions_folder(loaded_extension, folder_for_extension)
        self.__activate_extension(extension_uuid)

    def __get_version_of_extension(self, extension_uuid, extension_versions):
        available_versions = extension_versions.get(self.gnome_shell_version, None)
        if available_versions is None:
            raise ValueError('No versions of {} for gnome shell with version {} found!'.format(
                extension_uuid, self.gnome_shell_version)
            )
        else:
            return available_versions['version']

    def __load_extensions_archive(self, download_link):
        response = requests.get(download_link)
        temp_file_to_load = tempfile.NamedTemporaryFile(suffix='.zip')
        temp_file_to_load.write(response.content)
        return temp_file_to_load

    def __create_folder_for_extension(self, extension_uuid):
        full_path = os.path.join(self.install_path, extension_uuid)
        os.mkdir(full_path)
        return full_path

    def __unzip_extension_archive_to_extensions_folder(self, extension_archive, folder_to_unzip_into):
        zip_ref = zipfile.ZipFile(extension_archive, 'r')
        zip_ref.extractall(folder_to_unzip_into)
        zip_ref.close()

    def __activate_extension(self, extension_uuid):
        code = subprocess.call(['gnome-shell-extension-tool', '-e', extension_uuid])
        print(code)

    def get_data(self, extension_id):
        response = requests.get(self.EXTENSION_TPL.format(extension_id))
        soup = BeautifulSoup(response.text, features="html.parser")
        metadata = soup.findAll('div', {'class': ['extension', 'single-page']})[0]
        extension_uuid = metadata.attrs['data-uuid']
        extension_versions = json.loads(metadata.attrs['data-svm'])
        return extension_uuid, extension_versions

    def __process_args(self):
        self.parser.add_argument('extension_id', type=str, nargs='+')
        self.parser.add_argument('-v', '--version', '--gnome_shell_version', type=str)
        return self.parser.parse_args()

    def __get_install_path(self):
        return str(pathlib.Path.home() / '.local' / 'share' / 'gnome-shell' / 'extensions')


if __name__ == '__main__':
    App().process()
