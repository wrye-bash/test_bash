import unittest
from collections import OrderedDict
from pprint import pprint
from unittest import TestCase
import sys
from os.path import dirname, abspath, sep

mopy = dirname(dirname(dirname(abspath(__file__))))
assert mopy.split(sep)[-1].lower() == 'mopy'
sys.path.insert(0, mopy)
print 'Mopy folder inserted to path: ', mopy
# http://stackoverflow.com/q/40022220/281545
from bash.bosh import bsa_files

class TestBSAHeader(TestCase):
    def test_load_header(self):
        with open('F:\GAMES\TESIV\Oblivion\Data\Oblivion - Misc.bsa',
                  'r') as bsa:
            h = bsa_files.OblivionBsaHeader()
            h.load_header(bsa)
            assert h.file_id == bsa_files.OblivionBsaHeader.bsa_magic
            assert h.version == 103
            assert h.folder_records_offset == 36
            assert h.archive_flags == 1795
            assert h.folder_count == 10
            assert h.file_count == 115
            assert h.total_folder_name_length == 114
            assert h.total_file_name_length == 2084
            assert h.file_flags == 420

class TestBSAFolderRecord(TestCase):
    def test_load_folder_record(self):
        with open('F:\GAMES\TESIV\Oblivion\Data\Oblivion - Misc.bsa',
                  'r') as bsa:
            folder_rec = bsa_files.BSAFolderRecord()
            bsa.seek(36) # the size of the header
            folder_rec.load_record(bsa)
            assert folder_rec.hash == 0x6519496D057573
            assert folder_rec.files_count == 28
            assert folder_rec.file_records_offset == 2280

class TestOblivionBsa(TestCase):
    def test___init__(self):
        bsa = bsa_files.OblivionBsa(
            r'F:\GAMES\TESIV\Oblivion\Data\Oblivion - Misc.bsa')
        # pprint(bsa.bsa_folders)
        od = OrderedDict()
        for k, v in bsa.bsa_folders.iteritems():
            od[k] = (tuple(unicode(a) for a in v.assets.itervalues()))
        # pprint(od)
        assert od == Oblivion_Misc_bsa

class TestSkyrimBsa(TestCase):
    def test___init__(self):
        bsa = bsa_files.SkyrimBsa(
            r'F:\GAMES\Skyrim\Data\Skyrim - Interface.bsa')
        # pprint(bsa.bsa_folders)
        od = OrderedDict()
        for k, v in bsa.bsa_folders.iteritems():
            od[k] = (tuple(unicode(a) for a in v.assets.itervalues()))
        # pprint(od)
        assert od == Skyrim_Interface_bsa


Oblivion_Misc_bsa = OrderedDict([
    (u'menus', (
u'menus\\loading_bar_ingame_menu.xml', u'menus\\menu_labels.txt',
u'menus\\scroll_menu.xml', u'menus\\book_menu.xml',
u'menus\\persuasion_menu.xml', u'menus\\recharge_menu.xml',
u'menus\\birthsign_menu.xml', u'menus\\negotiate_menu.xml',
u'menus\\warning - changing these files.txt',
u'menus\\levelup_menu.xml', u'menus\\master_menu_file.txt',
u'menus\\sleep_wait_menu.xml', u'menus\\s.txt',
u'menus\\message_menu.xml', u'menus\\loading_ingame_menu.xml',
u'menus\\training_menu.xml', u'menus\\workbook.html',
u'menus\\loading_menu.xml', u'menus\\concat.bat',
u'menus\\ingredient_select_menu.xml', u'menus\\breath_meter_menu.xml',
u'menus\\quantity_menu.xml', u'menus\\repair_menu.xml',
u'menus\\container_menu.xml', u'menus\\vssver.scc',
u'menus\\strings.xml', u'menus\\class_menu.xml',
u'menus\\lockpick_menu.xml')),
    (u'fonts', (
u'fonts\\kingthings_regular.fnt',
u'fonts\\tahoma_bold_small_0_lod_a.tex',
u'fonts\\kingthings_shadowed_0_lod_a.tex', u'fonts\\daedric_font.fnt',
u'fonts\\handwritten_0_lod_a.tex', u'fonts\\handwritten.fnt',
u'fonts\\kingthings_regular_0_lod_a.tex',
u'fonts\\tahoma_bold_small.fnt', u'fonts\\kingthings_shadowed.fnt',
u'fonts\\daedric_font_0_lod_a.tex')),
    (u'menus\\prefabs', (
u'menus\\prefabs\\scroll_line.txt',
u'menus\\prefabs\\scroll_line.xml',
u'menus\\prefabs\\horiz_floating_scroll.xml',
u'menus\\prefabs\\xbox_floating_hint.xml',
u'menus\\prefabs\\page_tab.xml',
u'menus\\prefabs\\vertical_scroll.xml',
u'menus\\prefabs\\book_line.xml', u'menus\\prefabs\\fill_bar.xml',
u'menus\\prefabs\\button_short.xml',
u'menus\\prefabs\\button_floating.xml',
u'menus\\prefabs\\tile_button_over.xml',
u'menus\\prefabs\\vert_floating_scroll.xml',
u'menus\\prefabs\\button_floating_2.xml',
u'menus\\prefabs\\button_floating_3.xml',
u'menus\\prefabs\\button_xtralong.xml',
u'menus\\prefabs\\skill_item.xml',
u'menus\\prefabs\\generic_background.xml',
u'menus\\prefabs\\button_no_background.xml',
u'menus\\prefabs\\vssver.scc', u'menus\\prefabs\\tile_button.xml',
u'menus\\prefabs\\button_long.xml',
u'menus\\prefabs\\horizontal_scroll.xml',
u'menus\\prefabs\\focus_box.xml',
u'menus\\prefabs\\item_listing.xml')),
    (u'menus\\main', (
u'menus\\main\\copy of stats_menu.txt',
u'menus\\main\\player_model.xml',
u'menus\\main\\hud_main_menu.xml',
u'menus\\main\\hud_main_menu(2).xml',
u'menus\\main\\hud_info_menu.xml',
u'menus\\main\\quickkeys_menu.xml', u'menus\\main\\safe_zone.xml',
u'menus\\main\\hud_subtitle_menu.xml',
u'menus\\main\\magic_menu.xml', u'menus\\main\\vssver.scc',
u'menus\\main\\hud_reticle.xml',
u'menus\\main\\magic_popup_menu.xml',
u'menus\\main\\inventory_menu.xml', u'menus\\main\\map_menu.xml',
u'menus\\main\\stats_menu.xml')),
    (u'menus\\generic', (
u'menus\\generic\\test_menu.xml',
u'menus\\generic\\skill_perk.xml', u'menus\\generic\\vssver.scc',
u'menus\\generic\\quest_added.xml')),
    (u'menus\\options', (
u'menus\\options\\main_menu.xml',
u'menus\\options\\video_menu.xml',
u'menus\\options\\load_menu.xml',
u'menus\\options\\audio_menu.xml',
u'menus\\options\\xcontrols_menu.xml',
u'menus\\options\\credits_menu.xml',
u'menus\\options\\options_menu.xml',
u'menus\\options\\copy of main_menu.xml',
u'menus\\options\\vssver.scc',
u'menus\\options\\controls_menu.xml',
u'menus\\options\\save_menu.xml',
u'menus\\options\\downloads_menu.xml',
u'menus\\options\\pause_menu.xml',
u'menus\\options\\gameplay_menu.xml',
u'menus\\options\\video_display_menu.xml')),
    (u'menus\\chargen', (
u'menus\\chargen\\birthsign_menu.xml',
u'menus\\chargen\\skills_menu.xml',
u'menus\\chargen\\specilization_menu.xml',
u'menus\\chargen\\vssver.scc',
u'menus\\chargen\\attributes_menu.xml',
u'menus\\chargen\\class_menu.xml',
u'menus\\chargen\\race_sex_menu.xml')),
    (u'facegen', (u'facegen\\si.ctl',)),
    (u'menus\\message', (u'menus\\message\\message_menu.xml',)),
    (u'menus\\dialog', (
u'menus\\dialog\\sigilstone.xml',
u'menus\\dialog\\persuasion_menu.xml',
u'menus\\dialog\\dialog_menu.xml', u'menus\\dialog\\alchemy.xml',
u'menus\\dialog\\spell_purchase.xml',
u'menus\\dialog\\spellmaking.xml',
u'menus\\dialog\\enchantment.xml',
u'menus\\dialog\\enchantmentsetting_menu.xml',
u'menus\\dialog\\vssver.scc',
u'menus\\dialog\\texteditmenu.xml'))])

Skyrim_Interface_bsa = OrderedDict([
    (u'interface\\controls\\360', (
        u'interface\\controls\\360\\keyboard_english.txt',
        u'interface\\controls\\360\\gamepad.txt',
        u'interface\\controls\\360\\controlmap.txt')),
    (u'interface\\controls\\ps3', (
    u'interface\\controls\\ps3\\keyboard_english.txt',
    u'interface\\controls\\ps3\\gamepad.txt',
    u'interface\\controls\\ps3\\controlmap.txt')),
    (u'interface\\exported', (
        u'interface\\exported\\360_rb.png.dds',
        u'interface\\exported\\hudmenu.gfx',
        u'interface\\exported\\safezone.gfx',
        u'interface\\exported\\360_rs.png.dds',
        u'interface\\exported\\360_rt.png.dds',
        u'interface\\exported\\l-alt.png.dds',
        u'interface\\exported\\r-alt.png.dds',
        u'interface\\exported\\l-shift.png.dds',
        u'interface\\exported\\r-shift.png.dds',
        u'interface\\exported\\comma.png.dds',
        u'interface\\exported\\capslock.png.dds',
        u'interface\\exported\\right.png.dds',
        u'interface\\exported\\ps3_l3.png.dds',
        u'interface\\exported\\left.png.dds',
        u'interface\\exported\\period.png.dds',
        u'interface\\exported\\space.png.dds',
        u'interface\\exported\\ps3_lb.png.dds',
        u'interface\\exported\\ps3_r3.png.dds',
        u'interface\\exported\\mousemove.png.dds',
        u'interface\\exported\\360_ltrt.png.dds',
        u'interface\\exported\\equal.png.dds',
        u'interface\\exported\\ps3_ls.png.dds',
        u'interface\\exported\\ps3_lt.png.dds',
        u'interface\\exported\\ps3_rb.png.dds',
        u'interface\\exported\\hudmenu_i29e.dds',
        u'interface\\exported\\hudmenu_i2a1.dds',
        u'interface\\exported\\hudmenu_i2a7.dds',
        u'interface\\exported\\hudmenu_i2aa.dds',
        u'interface\\exported\\hudmenu_i2bb.dds',
        u'interface\\exported\\hudmenu_i2c1.dds',
        u'interface\\exported\\hudmenu_i2c7.dds',
        u'interface\\exported\\hudmenu_i2cd.dds',
        u'interface\\exported\\mouse.png.dds',
        u'interface\\exported\\ps3_rs.png.dds',
        u'interface\\exported\\ps3_rt.png.dds',
        u'interface\\exported\\tutorialmenu.gfx',
        u'interface\\exported\\tab.png.dds',
        u'interface\\exported\\bracketleft.png.dds',
        u'interface\\exported\\backspace.png.dds',
        u'interface\\exported\\360_a.png.dds',
        u'interface\\exported\\360_b.png.dds',
        u'interface\\exported\\ps3_ltrt.png.dds',
        u'interface\\exported\\textentry.gfx',
        u'interface\\exported\\enter.png.dds',
        u'interface\\exported\\quotesingle.png.dds',
        u'interface\\exported\\m1m2.png.dds',
        u'interface\\exported\\360_x.png.dds',
        u'interface\\exported\\360_y.png.dds',
        u'interface\\exported\\l-ctrl.png.dds',
        u'interface\\exported\\r-ctrl.png.dds',
        u'interface\\exported\\bracketright.png.dds',
        u'interface\\exported\\ps3_a.png.dds',
        u'interface\\exported\\ps3_b.png.dds',
        u'interface\\exported\\mouse1.png.dds',
        u'interface\\exported\\mouse2.png.dds',
        u'interface\\exported\\mouse3.png.dds',
        u'interface\\exported\\mouse4.png.dds',
        u'interface\\exported\\mouse5.png.dds',
        u'interface\\exported\\mouse6.png.dds',
        u'interface\\exported\\mouse7.png.dds',
        u'interface\\exported\\mouse8.png.dds',
        u'interface\\exported\\ps3_x.png.dds',
        u'interface\\exported\\ps3_y.png.dds',
        u'interface\\exported\\f10.png.dds',
        u'interface\\exported\\f11.png.dds', u'interface\\exported\\0.png.dds',
        u'interface\\exported\\1.png.dds', u'interface\\exported\\2.png.dds',
        u'interface\\exported\\3.png.dds', u'interface\\exported\\4.png.dds',
        u'interface\\exported\\5.png.dds', u'interface\\exported\\6.png.dds',
        u'interface\\exported\\7.png.dds', u'interface\\exported\\8.png.dds',
        u'interface\\exported\\9.png.dds', u'interface\\exported\\a.png.dds',
        u'interface\\exported\\b.png.dds', u'interface\\exported\\c.png.dds',
        u'interface\\exported\\d.png.dds', u'interface\\exported\\e.png.dds',
        u'interface\\exported\\f.png.dds', u'interface\\exported\\g.png.dds',
        u'interface\\exported\\h.png.dds', u'interface\\exported\\i.png.dds',
        u'interface\\exported\\j.png.dds', u'interface\\exported\\k.png.dds',
        u'interface\\exported\\l.png.dds', u'interface\\exported\\m.png.dds',
        u'interface\\exported\\n.png.dds', u'interface\\exported\\o.png.dds',
        u'interface\\exported\\p.png.dds', u'interface\\exported\\q.png.dds',
        u'interface\\exported\\r.png.dds', u'interface\\exported\\s.png.dds',
        u'interface\\exported\\t.png.dds', u'interface\\exported\\u.png.dds',
        u'interface\\exported\\v.png.dds', u'interface\\exported\\w.png.dds',
        u'interface\\exported\\x.png.dds', u'interface\\exported\\y.png.dds',
        u'interface\\exported\\z.png.dds', u'interface\\exported\\f12.png.dds',
        u'interface\\exported\\360_back.png.dds',
        u'interface\\exported\\ps3_lbrb.png.dds',
        u'interface\\exported\\diamondmarker.dds',
        u'interface\\exported\\hyphen.png.dds',
        u'interface\\exported\\esc.png.dds',
        u'interface\\exported\\f1.png.dds', u'interface\\exported\\f2.png.dds',
        u'interface\\exported\\f3.png.dds', u'interface\\exported\\f4.png.dds',
        u'interface\\exported\\f5.png.dds', u'interface\\exported\\f6.png.dds',
        u'interface\\exported\\f7.png.dds', u'interface\\exported\\f8.png.dds',
        u'interface\\exported\\f9.png.dds',
        u'interface\\exported\\tilde.png.dds',
        u'interface\\exported\\ps3_start.png.dds',
        u'interface\\exported\\slash.png.dds',
        u'interface\\exported\\semicolon.png.dds',
        u'interface\\exported\\up.png.dds',
        u'interface\\exported\\ps3_back.png.dds',
        u'interface\\exported\\360_l3.png.dds',
        u'interface\\exported\\down.png.dds',
        u'interface\\exported\\racesex_menu.gfx',
        u'interface\\exported\\360_lb.png.dds',
        u'interface\\exported\\360_r3.png.dds',
        u'interface\\exported\\backslash.png.dds',
        u'interface\\exported\\360_ls.png.dds',
        u'interface\\exported\\360_lt.png.dds',
        u'interface\\exported\\quest_journal.gfx',
        u'interface\\exported\\360_start.png.dds')),
    (u'strings', (
        u'strings\\skyrim_german.strings',
        u'strings\\skyrim_english.ilstrings',
        u'strings\\skyrim_italian.dlstrings',
        u'strings\\skyrim_english.strings',
        u'strings\\skyrim_spanish.ilstrings',
        u'strings\\skyrim_spanish.strings',
        u'strings\\skyrim_italian.ilstrings',
        u'strings\\skyrim_italian.strings',
        u'strings\\skyrim_french.dlstrings',
        u'strings\\skyrim_french.ilstrings',
        u'strings\\skyrim_german.dlstrings', u'strings\\skyrim_french.strings',
        u'strings\\skyrim_english.dlstrings',
        u'strings\\skyrim_german.ilstrings',
        u'strings\\skyrim_spanish.dlstrings')),
    (u'interface\\inventory components', (
        u'interface\\inventory components\\invertedinventorylists.swf',
        u'interface\\inventory components\\bottombar.swf',
        u'interface\\inventory components\\inventorylists.swf',
        u'interface\\inventory components\\itemcard.swf')),
    (u'interface', (
        u'interface\\widgetoverlay.swf', u'interface\\sleepwaitmenu.swf',
        u'interface\\containermenu.swf', u'interface\\fadermenu.swf',
        u'interface\\loadingmenu.swf', u'interface\\fonts_console.swf',
        u'interface\\giftmenu.swf', u'interface\\sharedcomponents.swf',
        u'interface\\cursormenu.swf', u'interface\\fonts_en.swf',
        u'interface\\tweenmenu.swf', u'interface\\startmenu.swf',
        u'interface\\messagebox.swf', u'interface\\bookmenu.swf',
        u'interface\\lockpickingmenu.swf', u'interface\\credits.txt',
        u'interface\\levelupmenu.swf', u'interface\\creditsmenu.swf',
        u'interface\\credits_french.txt', u'interface\\map.swf',
        u'interface\\book.swf', u'interface\\magicmenu.swf',
        u'interface\\favoritesmenu.swf', u'interface\\statsmenu.swf',
        u'interface\\dialoguemenu.swf', u'interface\\titles.swf',
        u'interface\\trainingmenu.swf', u'interface\\craftingmenu.swf',
        u'interface\\inventorymenu.swf', u'interface\\fontconfig.txt',
        u'interface\\bartermenu.swf', u'interface\\console.swf')),
    (u'interface\\controls\\pc', (
        u'interface\\controls\\pc\\keyboard_english.txt',
        u'interface\\controls\\pc\\keyboard_spanish.txt',
        u'interface\\controls\\pc\\keyboard_italian.txt',
        u'interface\\controls\\pc\\gamepad.txt',
        u'interface\\controls\\pc\\keyboard_french.txt',
        u'interface\\controls\\pc\\mouse.txt',
        u'interface\\controls\\pc\\keyboard_german.txt',
        u'interface\\controls\\pc\\controlmap.txt'))])

if __name__ == '__main__':
    unittest.main()
