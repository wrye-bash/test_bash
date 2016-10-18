import unittest
from collections import OrderedDict
from unittest import TestCase
import sys
from os.path import dirname, abspath, join, sep

mopy = dirname(dirname(dirname(abspath(__file__))))
assert mopy.split(sep)[-1].lower() == 'mopy'
bash_source = join(mopy, 'bash')
print sys.path
sys.path.insert(0, mopy)
print sys.path
print 'Mopy folder appended to path: ', mopy
print 'top_package', __name__.split('.')[0]
print __name__
# http://stackoverflow.com/q/40022220/281545
from bash.bosh import bsa_files

class TestBSAHeader(TestCase):
    def test_load_header(self):
        with open('F:\GAMES\TESIV\Oblivion\Data\Oblivion - Misc.bsa',
                  'r') as bsa:
            h = bsa_files.BSAHeader()
            h.load_header(bsa)
            assert h.file_id == 4281154
            assert h.version == 103
            assert h.folder_record_offset == 36
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

if __name__ == '__main__':
    # from os import sys, path
    # sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(
    # __file__)))))
    unittest.main()

class TestBSA(TestCase):
    def test___init__(self):
        bsa = bsa_files.BSA('F:\GAMES\TESIV\Oblivion\Data\Oblivion - Misc.bsa')
        # pprint(bsa.bsa_folders)
        od = OrderedDict()
        for k, v in bsa.bsa_folders.iteritems():
            od[k] = (tuple(unicode(a) for a in v.assets.itervalues()))
        # pprint(od)
        assert od == Oblivion_Misc_bsa


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
