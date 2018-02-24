# -*- coding: utf-8 -*-

#__author__ = 'Toril Rygg and Steinar Nerhus'
#__email__  = ''

from distutils.core import setup
from glob import glob
import sys
import py2exe

sys.path.append('C:\dlls')

gui = {
    'script' : 'GaiaMapGenerator.py',
    'icon_resources' : [(1, 'images\gaia_icon.ico'),
                        (2, 'images\hexagon_icon.ico'),
                        (3, 'images\\tech_icon.ico')],
}

data_files = [
    ('images', glob('images/*.*')),
]

py2exe_excludes = [
    '_socket',
    '_gtkagg',
    '_tkagg',
    'bsddb',
    'curses',
    'email',
    'pywin.debugger',
    'pywin.debugger.dbgcon',
    'pywin.dialogs',
    'tcl',
    'Tkconstants',
    'Tkinter',
]

py2exe_includes = [
    #'scipy.sparse.csgraph._validation',
    #'scipy.special._ufuncs_cxx',
]

setup(
    name = 'Stones',
    options = {
        'py2exe': {
            'excludes' : py2exe_excludes,
            'includes' : py2exe_includes,
        }
    },
    windows = [gui],
    data_files = data_files,
    requires=['os', 'wx']
)