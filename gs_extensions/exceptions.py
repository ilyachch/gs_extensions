class GnomeShellNotInstalledError(RuntimeError):
    pass


class ExtensionNotFoundInHub(RuntimeError):
    pass


class NoExtensionVersionForGnomeShell(RuntimeError):
    pass


class ExtensionAlreadyLoaded(RuntimeError):
    pass


class ExtensionAlreadyActivated(RuntimeError):
    pass
