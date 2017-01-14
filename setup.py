#!/usr/bin/env python
# vim:fileencoding=utf-8:noet
from __future__ import unicode_literals
import os
import sys

from setuptools import setup, find_packages
from setuptools.command.install import install

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.md'), 'rb').read().decode('utf-8')
except IOError:
    README = ''

class new_install(install):
    def run(self):
        print( self.root )
        install.run(self) # invoke original install

        # `sudo python ... install` not necesarily safe (don't want in system location) ?
        # Also, Mac OS has SIP as of El Capitan, which some may not have disabled

        #root = self.root or '/'
        root = os.path.expanduser('~')
        self.mkpath(os.path.join(root, '.config/themer/'))
        #self.mkpath(os.path.join(root, 'usr/share/fish/completions'))
        self.copy_tree('data/default', os.path.join(root, '.config/themer/'))
        #self.copy_file('data/fish/themer.fish', os.path.join(root, 'usr/share/fish/completions/'))

setup(
    name='Themer',
    version='1.6',
    description='Themer is a colorscheme generator and manager for your desktop.',
    long_description=README,
    author='Charles Leifer, Sol Bekic',
    author_email='s0lll0s@blinkenshell.org',
    url='https://github.com/S0lll0s/themer',
    scripts=['scripts/themer'],
    license='MIT',
    keywords='wm colorscheme color theme wallpaper',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    install_requires=['pyyaml','jinja2','pillow', 'requests'],
    cmdclass=dict(install=new_install)
)
