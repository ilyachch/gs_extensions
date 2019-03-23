# gs_extensions

CLI utility to manage gnome shell extensions

Allows to install gnome shell extensions from terminal or sh script.

## Installation

To install run:

```bash
$ pip install gs_extensions
```

## Usage:

To view the list of installed extensions:

```bash
$ gs_extensions dump
```

To make a file with list of installed extensions:

```bash
$ gs_extensions dump > extensions.txt
```

To install extensions from file:

```bash
$ gs_extensions install -r extensions.txt
```

To install extensions by uuid (if you know extension's UUID):

```bash
$ gs_extensions install user-theme@gnome-shell-extensions.gcampax.github.com [places-menu@gnome-shell-extensions.gcampax.github.com caffeine@patapon.info]
```

To install extension by their IDs (you can find this ids in browser i.e. `https://extensions.gnome.org/extension/19/user-themes/`):

```bash
$ gs_extensions install 19 [8 6] -i
```
