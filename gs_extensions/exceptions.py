class GnomeShellNotInstalledError(RuntimeError):
    pass


class ExtensionNotFoundInHub(RuntimeError):
    pass


class NoExtensionVersionForGnomeShell(RuntimeError):
    pass
