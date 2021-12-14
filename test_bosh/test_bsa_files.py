import filecmp
import inspect
import os
import unittest
from collections import OrderedDict
from pprint import pprint
from unittest import TestCase
import sys
from os.path import dirname, abspath, sep

import itertools

import struct as _struct

from test_bash.test_bosh.test_bsa_files_constants import \
    Skyrim_Interface_bsa, Oblivion_Misc_bsa, HeartOftheDead_Folder_Names, \
    MidasSpells, SkyrimSETextures8, HodBsa, MidasBsa

# TODO: flesh out fallout4 tests

mopy = dirname(dirname(dirname(abspath(__file__))))
assert mopy.split(sep)[-1].lower() == 'mopy'
sys.path.insert(0, mopy)
print 'Mopy folder inserted to path: ', mopy
# http://stackoverflow.com/q/40022220/281545
from bash.bosh import bsa_files

def get_script_dir(follow_symlinks=True):
    # http://stackoverflow.com/a/22881871/281545
    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)

this_script_dir = get_script_dir()
# print get_script_dir()

pjoin = os.path.join

resources_root = pjoin(this_script_dir , r'resources') #os.path.abspath('resources')
cache_root = pjoin(this_script_dir , r'bsa_cache')

# Some random records from the bsas to test those are read ok in _load_bsa
ob_rec = bsa_files.BSAFileRecord()
ob_rec.hash = 8316439984031428212
ob_rec.file_size_flags = 14632
ob_rec.raw_file_data_offset = 2704612
ob_rec = (u'fonts', u'daedric_font.fnt', ob_rec)

hod_rec = bsa_files.BSAFileRecord()
hod_rec.hash = 7255635117157822828
hod_rec.file_size_flags = 10017
hod_rec.raw_file_data_offset = 259709520
hod_rec = (u'meshes\characters\\ren\eyes', u'ren_eye01l.nif', hod_rec)

midas_rec = bsa_files.BSAFileRecord()
midas_rec.hash = 1382942182235694450
midas_rec.file_size_flags = 1662
midas_rec.raw_file_data_offset = 36787161
midas_rec = (u'meshes\characters\midaswreyth', u'midasteethlower.nif', midas_rec)

skyrim_rec = bsa_files.BSAFileRecord()
skyrim_rec.hash = 12662062996181901680
skyrim_rec.file_size_flags = 5479
skyrim_rec.raw_file_data_offset = 9285
skyrim_rec = (u'interface\\controls\\360', u'controlmap.txt', skyrim_rec)

skyrimse_rec = bsa_files.BSAFileRecord()
skyrimse_rec.hash = 2805577329219973297
skyrimse_rec.file_size_flags = 40341
skyrimse_rec.raw_file_data_offset = 20283702
skyrimse_rec = (u'textures\\_byoh\\clutter', u'breadpeel01.dds', skyrimse_rec)

# fallout4_rec = bsa_files.BSAFileRecord()
# fallout4_rec.hash = 8316439984031428212
# fallout4_rec.file_size_flags = 14632
# fallout4_rec.raw_file_data_offset = 2704612

class TestBSAHeader(TestCase):
    def test_load_header(self):
        with open(r'F:\GAMES\TESIV\Oblivion\Data\Oblivion - Misc.bsa',
                  'rb') as bsa:
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
        with open(r'F:\GAMES\TESIV\Oblivion\Data\Oblivion - Misc.bsa',
                  u'rb') as bsa:
            folder_rec = bsa_files.BSAFolderRecord()
            bsa.seek(36) # the size of the header
            folder_rec.load_record(bsa)
            assert folder_rec.hash == 0x6519496D057573
            assert folder_rec.files_count == 28
            assert folder_rec.file_records_offset == 2280

class _TestExtractMixin(object):
    assets_to_extract = None
    game_folder = 'Override'

    @property
    def extract_dir(self): return pjoin(cache_root, self.game_folder)
    @property
    def resources_dir(self): return pjoin(resources_root, self.game_folder)

    def test_extract_assets(self):
        bsa = self.bsa_type(self.bsa_path)
        bsa.extract_assets(self.assets_to_extract, self.extract_dir)
        for f in self.assets_to_extract:
            assert filecmp.cmp(pjoin(self.extract_dir, f),
                               pjoin(self.resources_dir, f),
                               shallow=False)

class TestOblivionBsa(TestCase):
    bsa_path = r'F:\GAMES\TESIV\Oblivion\Data\Oblivion - Misc.bsa'
    dict_file = Oblivion_Misc_bsa
    bsa_type = bsa_files.OblivionBsa
    file_rec = ob_rec
    # Hash values from Oblivion - used for testing calculate_hash
    # Dumped using BSArch from Oblivion GOTY Edition on Steam
    # A folder is always the place where the file below it came from
    hashes = [(r'textures\characters\darkelf', 0x25577CD741B6C66),
              (r'headdarkelff30.dds', 0x5D94602A680EB3B0),
              (r'textures\architecture\castleinterior', 0xA49973E74246F72),
              (r'castlestoneborder01.dds', 0x3F09D69B6313B0B1),
              (r'textures\menus80\alchemy', 0x432367574186D79),
              (r'alchemy (zoom).txt', 0x35A54934610E6D29),
              (r'meshes\armor\thief\f', 0x1EB279056D145C66),
              (r'cuirass.nif', 0x0A9125A06307F373),
              (r'meshes\clothes\amulet', 0xAF1AED2B6D156574),
              (r'amuletofkings.nif', 0x1852EA03610DE773),
              (r'meshes\creatures\spriggan\idleanims', 0xB38049296D236D73),
              (r'getupfaceup.kf', 0x0C113DB0670B75F0),
              (r'meshes\creatures\flameatronach', 0xB6D2FE3A6D1E6368),
              (r'backward.kf', 0x06EC35BC620872E4),
              (r'meshes\creatures\ogre\idleanims', 0xC2E1A4936D1F6D73),
              (r'check.kf', 0x1779FDE6630563EB),
              (r'sound\fx\fst\snow', 0xB02B1B5A73116F77),
              (r'fst_snow_01.wav', 0xD64F075CE60B3031),
              (r'sound\fx\npc\imp\injured', 0xA1058BCD73186564),
              (r'npc_imp_injured_01.wav', 0x24C6193BEE123031)]

    def test___init__(self):
        bsa = self.bsa_type(self.bsa_path, names_only=False, load_cache=True)
        # pprint(bsa.bsa_folders)
        od = OrderedDict()
        for k, v in bsa.bsa_folders.items():
            od[k] = (tuple(pjoin(k, a) for a in v.folder_assets))
        # pprint(od)
        assert od == self.dict_file
        rec = bsa.bsa_folders[self.file_rec[0]].folder_assets[self.file_rec[1]]
        assert rec.hash == self.file_rec[2].hash
        assert rec.file_size_flags == self.file_rec[2].file_size_flags
        assert rec.raw_file_data_offset == self.file_rec[2].raw_file_data_offset

    def test___init__light(self):
        bsa = self.bsa_type(self.bsa_path, names_only=True, load_cache=True)
        assert bsa._filenames == list(
            itertools.chain.from_iterable(self.dict_file.values()))

    def test_calculate_hash(self):
        calculate_hash = bsa_files.OblivionBsa.calculate_hash
        for file_name, expected_hash in self.hashes:
            assert calculate_hash(file_name) == expected_hash

    def test_undo_alterations(self):
        # TODO This is hideous, we really have to make some custom BSAs instead
        # Will modify the textures BSA of whoever is running this test :(
        path = r'F:\GAMES\TESIV\Oblivion\Data\Oblivion - Textures - ' \
               r'Compressed.bsa'
        texture_bsa = bsa_files.OblivionBsa(path, load_cache=True,
                                            names_only=False)
        texture_bsa.undo_alterations()
        assert texture_bsa.abs_path.crc == 0xC768066C

class TestHeartOfTheDead(TestOblivionBsa):
    bsa_path = r'F:\GAMES\TESIV\Oblivion\Data\HeartOftheDead.bsa'
    dict_file = HodBsa
    folder_names = HeartOftheDead_Folder_Names
    file_rec = hod_rec

    def test_load_bsa_light_folder_names(self):
        self.bsa_folders = OrderedDict()
        with open(self.bsa_path, u'rb') as bsa:
            h = bsa_files.OblivionBsaHeader()
            h.load_header(bsa)
            folder_records = [] # we need those to parse the folder names
            for __ in range(h.folder_count):
                rec = bsa_files.BSAFolderRecord()
                try:
                    rec.load_record(bsa)
                except Exception as e:
                    print __, e
                folder_records.append(rec)
            # load the file record block
            total_size = total_name_size = 0
            for folder_record in folder_records:
                name_size = _struct.unpack('B', bsa.read(1))[0]
                folder_path = bsa_files._decode_path(
                    _struct.unpack(u'%ds' % (name_size - 1),
                                   bsa.read(name_size - 1))[0])
                bsa.read(1)
                total_size += name_size + 1
                total_name_size += name_size
                current_folder = self.bsa_folders.setdefault(
                    folder_path, bsa_files.BSAFolder(folder_record))
                # print folder_path
                for __ in xrange(folder_record.files_count):
                    rec = bsa_files.BSAFileRecord()
                    rec.load_record(bsa)
                    file_name = u'?%d' % rec.hash
                    current_folder.folder_assets[file_name] = rec
                total_size+=folder_record.files_count *16
        print total_name_size
        print total_size
        print sum(k.files_count for k in folder_records)
        assert list(self.bsa_folders) == self.folder_names

class TestMidasSpells(TestHeartOfTheDead):
    bsa_path = r'F:\GAMES\TESIV\Oblivion\Data\MidasSpells.bsa'
    folder_names = MidasSpells
    dict_file = MidasBsa
    file_rec = midas_rec

class TestSkyrimBsa(_TestExtractMixin, TestOblivionBsa):
    bsa_path = r'F:\GAMES\Skyrim\Data\Skyrim - Interface.bsa'
    dict_file = Skyrim_Interface_bsa
    bsa_type = bsa_files.SkyrimBsa
    game_folder = 'Skyrim'
    file_rec = skyrim_rec
    assets_to_extract = {u'strings\\skyrim_german.strings',
                         u'strings\\skyrim_english.ilstrings',
                         u'strings\\skyrim_italian.dlstrings',
                         u'strings\\skyrim_english.strings',
                         u'strings\\skyrim_spanish.ilstrings',
                         u'strings\\skyrim_spanish.strings',
                         u'strings\\skyrim_italian.ilstrings',
                         u'strings\\skyrim_italian.strings',
                         u'strings\\skyrim_french.dlstrings',
                         u'strings\\skyrim_french.ilstrings',
                         u'strings\\skyrim_german.dlstrings',
                         u'strings\\skyrim_french.strings',
                         u'strings\\skyrim_english.dlstrings',
                         u'strings\\skyrim_german.ilstrings',
                         u'strings\\skyrim_spanish.dlstrings'}

class TestSkyrimSEBsaExtract(_TestExtractMixin, TestCase):
    bsa_path = r"F:\GAMES\The Elder Scrolls V Skyrim Special Edition\Data\Skyrim - Interface.bsa"
    bsa_type = bsa_files.SkyrimSeBsa
    game_folder = 'SkyrimSE'
    assets_to_extract = {u'strings\\skyrim_german.strings',
                         u'strings\\skyrim_english.ilstrings',
                         u'strings\\skyrim_italian.dlstrings',
                         u'strings\\skyrim_english.strings',
                         u'strings\\skyrim_spanish.ilstrings',
                         u'strings\\skyrim_spanish.strings',
                         u'strings\\skyrim_italian.ilstrings',
                         u'strings\\skyrim_italian.strings',
                         u'strings\\skyrim_french.dlstrings',
                         u'strings\\skyrim_french.ilstrings',
                         u'strings\\skyrim_german.dlstrings',
                         u'strings\\skyrim_french.strings',
                         u'strings\\skyrim_english.dlstrings',
                         u'strings\\skyrim_german.ilstrings',
                         u'strings\\skyrim_spanish.dlstrings',
                         u'strings\\skyrim_polish.strings',
                         u'strings\\skyrim_polish.dlstrings',
                         u'strings\\skyrim_polish.ilstrings',
                         u'strings\\skyrim_russian.strings',
                         u'strings\\skyrim_russian.dlstrings',
                         u'strings\\skyrim_russian.ilstrings',}

class TestSkyrimSEBsa(TestOblivionBsa):
    bsa_path = r"F:\GAMES\The Elder Scrolls V Skyrim Special Edition\Data\Skyrim - Textures8.bsa"
    dict_file = SkyrimSETextures8
    bsa_type = bsa_files.SkyrimSeBsa
    file_rec = skyrimse_rec

class TestFallout4Ba2(_TestExtractMixin, TestCase):
    bsa_path = r"F:\GAMES\FALLOUT 4\Data\Fallout4 - Interface.ba2"
    bsa_type = bsa_files.Fallout4Ba2
    game_folder = 'Fallout4'
    assets_to_extract = {u'Strings\\Fallout4_ja.DLSTRINGS',
                         u'Strings\\Fallout4_ja.ILSTRINGS',
                         u'Strings\\Fallout4_ja.STRINGS',}

    def test___init__(self):
        bsa = self.bsa_type(self.bsa_path, names_only=False, load_cache=True)
        # pprint(bsa.bsa_folders)
        # od = OrderedDict()
        # for k, v in bsa.bsa_folders.items():
        #     od[k] = (tuple(unicode(a) for a in v.assets.values()))
        # pprint(od)
        # assert od == Skyrim_Interface_bsa

    def test___init__light(self):
        bsa = bsa_files.Fallout4Ba2(self.bsa_path, names_only=True, load_cache=True)
        # print bsa._filenames

if __name__ == '__main__':
    unittest.main()
