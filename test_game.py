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
from unittest import TestCase

from bolt import GPath
from games import Game

class TestGame(TestCase):
    # def test__plugins_txt_modified(self):
    #     self.fail()
    #
    # def test_get_load_order(self):
    #     self.fail()
    #
    # def test__cached_or_fetch(self):
    #     self.fail()
    #
    # def test__save_fixed_load_order(self):
    #     self.fail()
    #
    # def test_set_load_order(self):
    #     self.fail()
    #
    # def test_pinned_mods(self):
    #     self.fail()
    #
    # def test_has_load_order_conflict(self):
    #     self.fail()
    #
    # def test_has_load_order_conflict_active(self):
    #     self.fail()
    #
    # def test_install_last(self):
    #     self.fail()
    #
    # def test_get_free_time(self):
    #     self.fail()
    #
    # def test__must_update_active(self):
    #     self.fail()
    #
    # def test_active_changed(self):
    #     self.fail()
    #
    # def test_load_order_changed(self):
    #     self.fail()
    #
    # def test_swap(self):
    #     self.fail()
    #
    # def test__fetch_load_order(self):
    #     self.fail()
    #
    # def test__fetch_active_plugins(self):
    #     self.fail()
    #
    # def test__persist_load_order(self):
    #     self.fail()
    #
    # def test__persist_active_plugins(self):
    #     self.fail()
    #
    # def test__persist_if_changed(self):
    #     self.fail()
    #
    # def test__parse_modfile(self):
    #     self.fail()
    #
    # def test__write_modfile(self):
    #     self.fail()
    #
    # def test__parse_plugins_txt(self):
    #     self.fail()
    #
    # def test__write_plugins_txt(self):
    #     self.fail()
    #
    # def test__fix_load_order(self):
    #     self.fail()
    #
    # def test__fix_active_plugins(self):
    #     self.fail()
    #
    # def test__order_fixed(self):
    #     self.fail()
    #
    # def test__check_active_order(self):
    #     self.fail()
    #
    # def test__index_of_first_esp(self):
    #     self.fail()

    def test__check_for_duplicates(self):
        a_ = map(GPath, ['a', 'b', 'c', 'a'])
        self.assertEqual(Game._check_for_duplicates(a_), {'a'})
        self.assertEqual(a_, map(GPath, ['a', 'b', 'c']))
        c_a_ = map(GPath, ['b', 'c', 'a', 'a', 'a', 'b', 'c', 'd', 'a'])
        self.assertEqual(Game._check_for_duplicates(c_a_), {'a', 'b', 'c'})
        self.assertEqual(c_a_, map(GPath, ['b', 'c', 'a', 'd']))
