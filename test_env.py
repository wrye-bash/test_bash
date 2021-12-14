# -*- coding: utf-8 -*-
#
# GPL License and Copyright Notice ============================================
#  This file is part of Wrye Bash.
#
#  Wrye Bash is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  Wrye Bash is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Wrye Bash; if not, write to the Free Software Foundation,
#  Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
#  Wrye Bash copyright (C) 2005-2009 Wrye, 2010-2021 Wrye Bash Team
#  https://github.com/wrye-bash
#
# =============================================================================
from functools import partial
from unittest import TestCase

import win32gui

import pywintypes

# wx.IconFromLocation(wx.IconLocation(r"C:\__\Mozilla Firefox\firefox.exe"))
import sys

def sys_encode(str_path):
    sys_encoded_path = str_path.encode(sys.getfilesystemencoding())
    #SHGetFileInfo doesn't work with Unix style paths
    sys_encoded_path = sys_encoded_path.replace('/', '\\')
    return sys_encoded_path

class TestExtractIcon(TestCase):
    # TODO: bundle some exe with icons and test that

    no_icons_exe = r"C:\__\Mozilla Firefox\plugin-container.exe"
    icons_exe = r"C:\__\Mozilla Firefox\firefox.exe"

    def test_ExtractIcon_non_existent(self):
        try:
            win32gui.ExtractIcon(0, self.no_icons_exe, 0)
        except Exception as e:
            # print e
            # (1813, 'ExtractIcon',
            # 'The specified resource type cannot be found in the image file.')
            self.assertIsInstance(e, pywintypes.error)

    def test_ExtractIcon_non_existent_file(self):
        try:
            win32gui.ExtractIcon(0, r'C:\not\a\path', 0)
        except Exception as e:
            # print e
            # (2, 'ExtractIcon', 'The system cannot find the file specified.')
            self.assertIsInstance(e, pywintypes.error)

    # win32gui.ExtractIconEx(target.s, iconIndex, numIcons)
    # numIcons must be >= 1 - other values raise value error
    # iconIndex must be -1 to get num of icons in the file or a number smaller
    # than win32gui.ExtractIconEx(target.s, -1) - other values result in
    # return value ([], [])
    get_non_existent_icon = partial(win32gui.ExtractIconEx, no_icons_exe)
    def test_ExtractIcon_existent(self):
        # NB: we should call DestroyIcon on returned handles !!!
        self.assertTrue(win32gui.ExtractIcon(0, self.icons_exe, 0))
        self.assertTrue(win32gui.ExtractIcon(0, self.icons_exe, 1))
        self.assertTrue(win32gui.ExtractIcon(0, self.icons_exe, 2))
        self.assertTrue(win32gui.ExtractIcon(0, self.icons_exe, 3))
        self.assertTrue(win32gui.ExtractIcon(0, self.icons_exe, 4))
        self.assertTrue(win32gui.ExtractIcon(0, self.icons_exe, 5))
        # there are only 6 icons
        self.assertFalse(win32gui.ExtractIcon(0, self.icons_exe, 6))

    def test_ExtractIconEx_numIcons(self):
        # numIcons must be >= 1 - other values raise ValueError
        numIcons = 0
        self.assertRaises(ValueError, self.get_non_existent_icon, 1, numIcons)
        numIcons = -1
        self.assertRaises(ValueError, self.get_non_existent_icon, 1, numIcons)
        # ValueError: Must supply a valid number of icons to fetch.
        #----------------------------------------------------------------------
        numIcons = 666 # large number is ok
        self.assertEqual(self.get_non_existent_icon(1, numIcons),
                         self.extractEx_empty)

    def test_ExtractIconEx_non_existent(self):
        # contains 0 icons
        self.assertEqual(self.get_non_existent_icon(-1, 1), 0)
        self.assertEqual(self.get_non_existent_icon(1, 1), ([], []))

    get_existent_icon = partial(win32gui.ExtractIconEx, icons_exe)
    # return value is ([icon handles], [icon handles]) - large, small
    # for large and small see:
    # https://msdn.microsoft.com/en-us/library/windows/desktop/ms648050(v=vs.85).aspx#_win32_Icon_Sizes
    extractEx_empty = ([], [])
    def test_ExtractIconEx_existent(self):
        # contains 0 icons
        numIcons = 6
        get_number_of_icons = -1
        self.assertEqual(self.get_existent_icon(get_number_of_icons, 1),
                         numIcons) # six icon pairs
        # asking for 7th icon pair returns empty (zero based !)
        self.assertEqual(self.get_existent_icon(numIcons, 1),
                         self.extractEx_empty)
        # asking for all six pairs starting from index 0,1,... returns
        # remaining ones. NB: handles must be destroyed !!!
        # print(self.get_existent_icon(0, numIcons))
        self.assertEqual(len(self.get_existent_icon(0, numIcons)[0]), 6)
        self.assertEqual(len(self.get_existent_icon(1, numIcons)[0]), 5)
        self.assertEqual(len(self.get_existent_icon(2, numIcons)[0]), 4)
        self.assertEqual(len(self.get_existent_icon(3, numIcons)[0]), 3)
        self.assertEqual(len(self.get_existent_icon(4, numIcons)[0]), 2)
        self.assertEqual(len(self.get_existent_icon(5, numIcons)[0]), 1)
        self.assertEqual(len(self.get_existent_icon(6, numIcons)[0]), 0)
        # asking for first pair (starting from first icon, 1 icon -> (0, 1))
        large, small = self.get_existent_icon(0, 1)
        self.assertEqual(len(large), 1)
        # print win32gui.GetIconInfo(large[0])
        # print win32gui.GetIconInfo(small[0])
        # now god knows what those icons are...

    def test_SHGetFileInfo(self):
        from win32com.shell import shell, shellcon
        shellcon_flags = shellcon.SHGFI_ICONLOCATION | \
                shellcon.SHGFI_SYSICONINDEX # | \
                # shellcon.SHGFI_DISPLAYNAME | \
        # shellcon_flags = shellcon.SHGFI_SYSICONINDEX
        def get_icon_info(str_path):
            sys_encoded_path = sys_encode(str_path)
            print shell.SHGetFileInfo(sys_encoded_path, 0, shellcon_flags)
        get_icon_info(r"C:\__\Mozilla Firefox\plugin-container.exe")
        get_icon_info(r"C:\__\Mozilla Firefox\firefox.exe")
        get_icon_info(r"C:\__\FLAC\flac.ico")
        get_icon_info(
            r"C:\Users\MrD\Desktop\Banquet_Louvre_Kylix_G133_by_Cage_Painter"
            r".jpg")
        get_icon_info(r"C:\Dropbox\Camera Uploads\2017-04-23 03.30.42.jpg")

    def test_SHGetFileInfo2(self):
        from win32com.shell import shell, shellcon
        shellcon_flags = shellcon.SHGFI_USEFILEATTRIBUTES | \
                         shellcon.SHGFI_SYSICONINDEX
        FILE_ATTRIBUTE_NORMAL = 128
        def get_icon_info(str_path):
            sys_encoded_path = sys_encode(str_path)
            print shell.SHGetFileInfo(sys_encoded_path, FILE_ATTRIBUTE_NORMAL, shellcon_flags)
        get_icon_info(r".exe")
        get_icon_info(r".exe")
        get_icon_info(r".ico")
        get_icon_info(r".jpg")
        get_icon_info(r"C:\Dropbox\Camera Uploads\2017-04-23 03.30.42.jpg")
