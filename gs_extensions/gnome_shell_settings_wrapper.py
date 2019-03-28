from gi.repository import Gio


class GnomeShellSettingsWrapper:
    ENABLED_EXTENSIONS_KEY = 'enabled-extensions'

    def __init__(self):
        self.__settings = Gio.Settings(schema='org.gnome.shell')
        self.__extensions_list = None

    def get_extensions(self):
        extensions_list = self.__settings.get_strv(self.ENABLED_EXTENSIONS_KEY)
        if self.__extensions_list is None:
            self.__extensions_list = extensions_list
        return self.__extensions_list

    def add_extension(self, extension):
        if extension not in self.__extensions_list:
            self.__extensions_list.append(extension)
        self.__settings.set_strv(self.ENABLED_EXTENSIONS_KEY, self.__extensions_list)
        return self.__extensions_list
