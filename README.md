# papis-firefox

## Description

papis-firefox is a Firefox add-on for integration with [Papis](https://github.com/papis/papis), a powerful command-line bibliography manager for Linux.
It allows to add an entry in Papis using the url of the current page.
It installs a button in the navigation bars that simply executes in a new terminal the command:
`papis add --from-url <url>`with <url> `<url>` being the url of the current tab or `papis add --from-doi <doi>` if a DOI is found in the url.
  
Due to the security restrictions on web extensions, the add-on cannot execute the command itself.
It requires a connector app written in Python.
The web extension sends thes url to the connector app, using *native messaging*, that executes the command.



## Installation of the Firefox add-on

Two ways:

1. Install it from the [Mozilla add-on page](https://addons.mozilla.org/addon/papis-connector/).

Or,

2. Create a zip from the source:
```
cd add-on
zip -r -FS ../papis-firefox.zip *
```
>The `.zip` package can then be installed through the **Add-ons** section of the Firefox menu.
If you choose this method, the add-on would not be signed.
To be installed, it is required to change the parameter `xpinstall.signatures.required preference`to false in [about:config](about:config). 
**Note that this change may create a security vulnerability on your system, use it at your own risks. Prefer the first option if you have no reason to do otherwise.**

## Installation of the Papis connector script

Copy the content of the `script` folder to your local papis script folder, for instance `~/.papis` or `~/.config/papis/scripts`.
Then execute the command:

```
papis install-webext
```
It will create a `papis_connector.json` file and copy it in the `.mozilla` local folder to allow the Firefox add-on to communicate with the connector app.
