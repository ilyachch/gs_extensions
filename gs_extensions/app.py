import argparse
import pathlib

from gs_extensions.gnome_shell_extension_wrapper import GnomeShellExtensionWrapper
from gs_extensions.gnome_shell_wrapper import GnomeShellWrapper


class App:
    ACTION_DUMP = 'dump'
    ACTION_INSTALL = 'install'

    def __init__(self):
        self.parser = argparse.ArgumentParser('CLI tool to install Gnome Shell Extensions.')
        self.args = self.__process_args()

        self.gnome_shell = GnomeShellWrapper()

    def process(self):
        if self.args.action == self.ACTION_DUMP:
            self.dump()
        elif self.args.action == self.ACTION_INSTALL and self.args.reverse is not None:
            self.revert_extensions()
        elif self.args.action == self.ACTION_INSTALL and not self.args.ids and len(self.args.extensions) > 0:
            self.install_extensions_by_uuid()
        elif self.args.action == self.ACTION_INSTALL and self.args.ids and len(self.args.extensions) > 0:
            self.install_extensions_by_ids()
        else:
            print(self.parser.print_help())

    def dump(self):
        for extension in self.gnome_shell.get_installed_extensions():
            print(extension.uuid)

    def revert_extensions(self):
        extensions_list = self.gnome_shell.get_extensions_from_file(self.args.reverse)
        for extension in extensions_list:
            extension.install()

    def install_extensions_by_uuid(self):
        extensions_list = [GnomeShellExtensionWrapper.from_uuid(uuid=uuid, gnome_shell=self.gnome_shell) for uuid in
                           self.args.extensions]
        for extension in extensions_list:
            extension.install()

    def install_extensions_by_ids(self):
        extensions_list = [GnomeShellExtensionWrapper.from_pk(pk=int(uuid), gnome_shell=self.gnome_shell) for uuid in
                           self.args.extensions]
        for extension in extensions_list:
            extension.install()

    def __process_args(self):
        self.parser.add_argument('action', type=str, choices=[self.ACTION_DUMP, self.ACTION_INSTALL])
        self.parser.add_argument('-i', '--ids', action='store_true', default=False)
        self.parser.add_argument('extensions', type=str, nargs='*')
        self.parser.add_argument('-r', '--reverse', type=pathlib.Path)
        return self.parser.parse_args()


def main():
    App().process()


if __name__ == '__main__':
    main()
