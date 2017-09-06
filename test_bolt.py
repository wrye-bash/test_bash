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
#  Wrye Bash copyright (C) 2005-2009 Wrye, 2010-2015 Wrye Bash Team
#  https://github.com/wrye-bash
#
# =============================================================================
from collections import OrderedDict
from unittest import TestCase

from bolt import LowerDict, DefaultLowerDict
# from bash.bosh.ini_files import _LowerOrderedDict # fails !

class TestLowerDict(TestCase):

    dict_type = LowerDict

    # def test__process_args(self):
    #     self.fail()

    def test___delitem__(self):
        a = self.dict_type()
        a.update(dict(sape=4139, guido=4127, jack=4098))
        del a['sAPe']
        self.assertFalse('sape' in a)
        del a['GUIDO']
        self.assertFalse('guido' in a)

    def test___getitem__(self):
        a = self.dict_type(dict(sape=4139, guido=4127, jack=4098))
        self.assertEqual(a['sape'], 4139)
        self.assertEqual(a['SAPE'], 4139)
        self.assertEqual(a['SAPe'], 4139)

    def test___init__(self):
        a = self.dict_type(dict(sape=4139, guido=4127, jack=4098))
        b = self.dict_type(sape=4139, guido=4127, jack=4098)
        c = self.dict_type([(u'sape', 4139), (u'guido', 4127), (u'jack', 4098)])
        d = self.dict_type(c)
        e = self.dict_type(c, sape=4139, guido=4127, jack=4098)
        # del e['JACK']
        f = e.copy()
        del f['JACK'] # BLOWS
        # del f['jack']
        f = self.dict_type(f, jack=4098)
        self.assertEqual(a, b)
        self.assertEqual(a, c)
        self.assertEqual(a, d)
        self.assertEqual(a, e)
        self.assertEqual(a, f)

    def test___setitem__(self):
        a = self.dict_type()
        a['sape'] = 4139
        self.assertEqual(a['sape'], 4139)
        self.assertEqual(a['SAPE'], 4139)
        self.assertEqual(a['SAPe'], 4139)
        a['sape'] = 'None'
        self.assertEqual(a['sape'], 'None')
        self.assertEqual(a['SAPE'], 'None')
        self.assertEqual(a['SAPe'], 'None')

    def test_fromkeys(self):
        a = self.dict_type(dict(sape=4139, guido=4139, jack=4139))
        c = self.dict_type.fromkeys(['sape', 'guido', 'jack'], 4139)
        self.assertEqual(a, c)
        c = self.dict_type.fromkeys(['sApe', 'guIdo', 'jaCK'], 4139)
        self.assertEqual(a, c)

    def test_get(self):
        a = self.dict_type(dict(sape=4139, guido=4127, jack=4098))
        self.assertEqual(a.get('sape'), 4139)
        self.assertEqual(a.get('SAPE'), 4139)
        self.assertEqual(a.get('SAPe'), 4139)

    def test_setdefault(self):
        a = self.dict_type()
        a['sape'] = 4139
        self.assertEqual(a.setdefault('sape'), 4139)
        self.assertEqual(a.setdefault('SAPE'), 4139)
        self.assertEqual(a.setdefault('SAPe'), 4139)
        self.assertEqual(a.setdefault('GUIDO', 4127), 4127)
        self.assertEqual(a.setdefault('guido'), 4127)
        self.assertEqual(a.setdefault('GUido'), 4127)

    def test_pop(self):
        a = self.dict_type()
        a['sape'] = 4139
        self.assertEqual(a['sape'], 4139)
        self.assertEqual(a['SAPE'], 4139)
        self.assertEqual(a['SAPe'], 4139)

    def test_update(self):
        a = self.dict_type()
        a.update(dict(sape=4139, guido=4127, jack=4098))
        self.assertEqual(a['sape'], 4139)
        self.assertEqual(a['SAPE'], 4139)
        self.assertEqual(a['guido'], 4127)
        self.assertEqual(a['GUido'], 4127)

    def test___repr__(self):
        a = self.dict_type()
        a.update(dict(sape=4139, guido=4127, jack=4098))
        from collections import defaultdict
        from bolt import CIstr
        self.assertEqual(eval(repr(a)), a)

class TestDefaultLowerDict(TestLowerDict):

    dict_type = DefaultLowerDict

    def test___init__(self):
        a = DefaultLowerDict(LowerDict, dict(sape=4139, guido=4127, jack=4098))
        b = DefaultLowerDict(LowerDict, sape=4139, guido=4127, jack=4098)
        c = DefaultLowerDict(LowerDict, [(u'sape', 4139), (u'guido', 4127), (u'jack', 4098)])
        d = DefaultLowerDict(LowerDict, c)
        e = DefaultLowerDict(LowerDict, c, sape=4139, guido=4127, jack=4098)
        f = e.copy()
        self.assertEqual(a, b)
        self.assertEqual(a, c)
        self.assertEqual(a, d)
        self.assertEqual(a, e)
        self.assertEqual(a, f)

    def test___getitem__(self):
        a = DefaultLowerDict(LowerDict, dict(sape=4139, guido=4127, jack=4098))
        self.assertEqual(a['sape'], 4139)
        self.assertEqual(a['SAPE'], 4139)
        self.assertEqual(a['SAPe'], 4139)
        self.assertEqual(a['NEW_KEY'], LowerDict())

    def test_get(self):
        a = DefaultLowerDict(int, dict(sape=4139, guido=4127, jack=4098))
        self.assertEqual(a.get('sape'), 4139)
        self.assertEqual(a.get('SAPE'), 4139)
        self.assertEqual(a.get('SAPe'), 4139)
        self.assertEqual(a.get('NEW_KEY'), None)

    def test_fromkeys(self):
        # see: defaultdict.fromkeys should accept a callable factory:
        # http://www.psf.upfronthosting.co.za/issue23372 (rejected)
        a = self.dict_type(int, dict(sape=4139, guido=4139, jack=4139))
        c = self.dict_type.fromkeys(['sape', 'guido', 'jack'], 4139)
        self.assertEqual(a, c) # !!!
        c = self.dict_type.fromkeys(['sApe', 'guIdo', 'jaCK'], 4139)
        self.assertEqual(a, c) # !!!
        # print c.default_factory # None !
        # print type(c)
        # print type(a)

class _LowerOrderedDict(LowerDict, OrderedDict): pass

class Test_LowerOrderedDict(TestLowerDict):

    dict_type = _LowerOrderedDict

    def test_keys(self):
        a = self.dict_type([(u'sape', 4139), (u'guido', 4127), (u'jack', 4098)])
        self.assertEqual(a.keys(), [u'sape', u'guido',u'jack'])
