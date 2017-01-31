Themer
======

This fork was only made for me to personally work on expanding Themer to Mac OS safely - it doesn't really represent much original work being done on the project itself. The original project and s-ol are still in active development.

*Themer is a colorscheme generator and manager for your desktop.*


Installation
------------

### AUR (Arch)

Install [python-themer-git](https://aur.archlinux.org/packages/python-themer-git/) with the AUR manager of your choice:

    $ yaourt -S python-themer-git


### PyPi

`themer` is now available in the PyPi repository as well. You can use a tool like `pip` to install it:

    $ pip install themer


### Manual Installation

First, check out the git repository:

    $ git clone https://github.com/S0lll0s/themer.git

Install with `python setup.py install`

    $ cd themer
    $ sudo python setup.py install


Configuration
-------------

You can create multiple template dirs for `themer` in `~/.config/themer/templates`.
The default template is `i3`; see [data/default](data/default) for the default configuration.


Usage
-----

### Integrating Themer with your Setup

All the following steps will show you how to use `themer` to generate themes,
but you also need to configure your DE to use the generated theme.

`themer` does not assume anything about the tools you use in your DE, you need to tell your DE about `themer`.
The current theme will always be available in `$XDG_HOME/themer/current` (usually `.config/themer/current`).
To use `themer`, symlink the seperate files from there to their destination.

For example, this is how to set up `i3` with `themer`:

    $ mkdir -p .i3
    $ ln -s ~/.config/themer/current/i3.conf .i3/config


### Generating Themes

Generate a theme from a wallpaper:

    $ themer generate themename wallpaper.png

...or install a colorscheme from `sweyla.com`:
 
    $ themer generate themename 693812

(this will install [http://sweyla.com/themes/seed/693812/](http://sweyla.com/themes/seed/693812/))

you can also use an Xresources-style file:

    $ themer generate themename /home/me/.Xresources

[Plugins](#plugins) enable you to generate themes from other sources as well, see below.


### Viewing Installed Themes

You can list all generated themes with `themer list`:

    $ themer list
    themeone
    themetwo


### Viewing Installed Plugins

    $ themer plugins
    Enabled activators:
      themer.activators.wallfix.WallfixActivator
      themer.activators.i3.I3Activator
    Enabled parsers:
      themer.parsers.SweylaColorParser
      themer.parsers.KmeansColorParser
      themer.parsers.CachedColorParser
      themer.ColorParser


### Activating Themes

You can activate an existing theme with `themer activate`:

    $ themer activate sometheme

This will symlink all defined templates to `~/.config/themer/current`. You should, in turn, symlink all the global configuration files to there. For example for i3:

    $ ln -s ~/.config/themer/current/i3.conf ~/.i3/config

To view the currently activated theme's colors use `themer current`.

If you have modified the templates, activating the theme again will not apply those changes. Instead
use `themer render` to update your configuration:

    $ themer render sometheme

You can also re-render all of your themes (for example if you changed a lot in your configuration) by supplying `all` instead of a theme's name:

    $ themer render all


### Deleting Themes

Deleting generated themes is possible using `themer delete`:

    $ themer delete sometheme


Screenshots
-----------

![](http://i.imgur.com/dXpXxPz.png)
![](http://i.imgur.com/axUuxbF.png)
![](http://media.charlesleifer.com/blog/photos/candybean.png)
![](http://media.charlesleifer.com/blog/photos/bloom.png)
![](http://media.charlesleifer.com/blog/photos/waves.png)
![](http://media.charlesleifer.com/blog/photos/waves2.png)
![](http://i.imgur.com/7GISqHw.png)
![](http://i.imgur.com/cutS0S7.png)


Plugins
-------

Plugins can be installed anywhere into your PYTHONPATH, but the `plugins` directory under the used template dir is automatically added to `sys.path`, so you may want to place them there (usually this is `~/.config/themer/templates/i3/plugins`).
They are loaded via their python module-an-classname string; e.g. `mymodule.activator.MyActivator`.
Plugins are configured on a template-directory basis, in the `config.yaml` file (default `~/.config/themer/templates/i3/config.yaml`).

There are two kinds of plugins: **Activators** and **Parsers**.
Activators should inherit from `themer.ThemeActivator`, Parsers should inherit from `themer.ColorParser`.


### `ThemeActivator`s
Activators are run once every time a theme is activated. Use them to reload configuration files, set desktop wallpapers etc.

Each Activator should implement the method `activate`.
The constructor is passed the values for `theme_name`, `theme_dir` and `logger`.
All of these and `colors` can be accessed via the instance's properties.


#### Example:

    from themer import ThemeActivator
    import os
    
    class I3Activator(ThemeActivator):
        def activate(self):
            os.system('i3-msg -q restart')


### `ColorParser`s
Parsers are used to generate colorschemes from files and strings.

Each ColorParser should implement the method `read`, which should return the color dictionary generated from the input string in `self.data` (or obtained via the constructor's first argument).
A ColorParser can additionally return a path to a wallpaper to be used by setting `self.wallpaper` to anything other than `None`.

Additionally, Parsers need to have a `check` attribute. It is used to determine whether a Parser should be used for a given color source. `check` can either be a function, in which case it is passed the color-source string and expected to return a truthy value if it wants to handle that color source, or a string.
If it is a string it will be used as a regex and matched against the color source string.

The `themer.check_file_regex` helper can be used to build a `check` function that checks filenames against a regex and verifies their existence on the filesystem.

The constructor is passed the values for `data`, `config` and `logger`.
All of these can be accessed via the instance's properties.
The default constructor also sets `self.colors` to a new dictionary and `self.wallpaper` to `None`.


#### Example:

    from themer import ColorParser, check_file_regex

    class NewColorParser(ColorParser):
        check = check_file_regex('\.yaml$')
        def read(self):
            with open(self.data) as fh: # load colors from a yaml file
                self.colors = yaml.load(fh)
            return self.colors


Credits
-------

Original script by [Charles Leifer](https://github.com/coleifer)  
Maintained and developed further by [Sol Bekic](https://github.com/S0lll0s)
