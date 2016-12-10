import filecmp
import os
import unittest
from collections import OrderedDict
from pprint import pprint
from unittest import TestCase
import sys
from os.path import dirname, abspath, sep

import itertools

import struct

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

resources_root = ur'C:\Dropbox\eclipse_workspaces\python\wrye-bash\Mopy\test_bash\test_bosh\resources' #os.path.abspath('resources')

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
        with open('F:\GAMES\TESIV\Oblivion\Data\Oblivion - Misc.bsa',
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
        with open('F:\GAMES\TESIV\Oblivion\Data\Oblivion - Misc.bsa',
                  'rb') as bsa:
            folder_rec = bsa_files.BSAFolderRecord()
            bsa.seek(36) # the size of the header
            folder_rec.load_record(bsa)
            assert folder_rec.hash == 0x6519496D057573
            assert folder_rec.files_count == 28
            assert folder_rec.file_records_offset == 2280

class _TestExtractMixin(object):
    assets_to_extract = None

    def test_extract_assets(self):
        bsa = self.bsa_type(self.bsa_path)
        bsa.extract_assets(self.assets_to_extract, self.extract_dir)
        for f in self.assets_to_extract:
            assert filecmp.cmp(os.path.join(self.extract_dir, f),
                               os.path.join(self.resources_dir, f),
                               shallow=False)

class TestOblivionBsa(TestCase):
    bsa_path = r'F:\GAMES\TESIV\Oblivion\Data\Oblivion - Misc.bsa'
    dict_file = Oblivion_Misc_bsa
    bsa_type = bsa_files.OblivionBsa
    file_rec = ob_rec

    def test___init__(self):
        bsa = self.bsa_type(self.bsa_path, names_only=False, load_cache=True)
        # pprint(bsa.bsa_folders)
        od = OrderedDict()
        for k, v in bsa.bsa_folders.iteritems():
            od[k] = (tuple(unicode(a) for a in v.assets.itervalues()))
        # pprint(od)
        assert od == self.dict_file
        rec = bsa.bsa_folders[self.file_rec[0]].assets[self.file_rec[1]].filerecord
        assert rec.hash == self.file_rec[2].hash
        assert rec.file_size_flags == self.file_rec[2].file_size_flags
        assert rec.raw_file_data_offset == self.file_rec[2].raw_file_data_offset

    def test___init__light(self):
        bsa = self.bsa_type(self.bsa_path, names_only=True, load_cache=True)
        assert bsa._filenames == list(
            itertools.chain.from_iterable(self.dict_file.values()))


class TestHeartOfTheDead(TestOblivionBsa):
    bsa_path = r'F:\GAMES\TESIV\Oblivion\Data\HeartOftheDead.bsa'
    dict_file = HodBsa
    folder_names = HeartOftheDead_Folder_Names
    file_rec = hod_rec

    def test_load_bsa_light_folder_names(self):
        self.bsa_folders = OrderedDict()
        with open(self.bsa_path, 'rb') as bsa:
            h = bsa_files.OblivionBsaHeader()
            h.load_header(bsa)
            folder_records = [] # we need those to parse the folder names
            for __ in xrange(h.folder_count):
                rec = bsa_files.BSAFolderRecord()
                try:
                    rec.load_record(bsa)
                except Exception as e:
                    print __, e
                folder_records.append(rec)
            # load the file record block
            total_size = total_name_size = 0
            for folder_record in folder_records:
                name_size = struct.unpack('B', bsa.read(1))[0]
                folder_path = bsa_files._decode_path(
                    struct.unpack('%ds' % (name_size - 1),
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
                    current_folder.assets[file_name] = bsa_files.BSAAsset(
                        os.path.sep.join((folder_path, file_name)), rec)
                total_size+=folder_record.files_count *16
        print total_name_size
        print total_size
        print sum(k.files_count for k in folder_records)
        assert self.bsa_folders.keys() == self.folder_names

class TestMidasSpells(TestHeartOfTheDead):
    bsa_path = r'F:\GAMES\TESIV\Oblivion\Data\MidasSpells.bsa'
    folder_names = MidasSpells
    dict_file = MidasBsa
    file_rec = midas_rec

class TestSkyrimBsa(_TestExtractMixin, TestOblivionBsa):
    bsa_path = r'F:\GAMES\Skyrim\Data\Skyrim - Interface.bsa'
    dict_file = Skyrim_Interface_bsa
    bsa_type = bsa_files.SkyrimBsa
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
    extract_dir = os.path.abspath('bsa_cache/Skyrim')
    resources_dir = os.path.join('resources/Skyrim')

class TestSkyrimSEBsaExtract(_TestExtractMixin, TestCase):
    bsa_path = r"F:\GAMES\The Elder Scrolls V Skyrim Special Edition\Data\Skyrim - Interface.bsa"
    bsa_type = bsa_files.SkyrimSeBsa
    extract_dir = os.path.abspath('bsa_cache/SkyrimSE')
    resources_dir = os.path.join('resources/SkyrimSE')
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
    assets_to_extract = {u'Strings\\Fallout4_ja.DLSTRINGS',
                         u'Strings\\Fallout4_ja.ILSTRINGS',
                         u'Strings\\Fallout4_ja.STRINGS',}
    extract_dir = os.path.abspath('bsa_cache/Fallout4')
    resources_dir = os.path.join('resources/Fallout4')

    def test___init__(self):
        bsa = self.bsa_type(self.bsa_path, names_only=False, load_cache=True)
        # pprint(bsa.bsa_folders)
        # od = OrderedDict()
        # for k, v in bsa.bsa_folders.iteritems():
        #     od[k] = (tuple(unicode(a) for a in v.assets.itervalues()))
        # pprint(od)
        # assert od == Skyrim_Interface_bsa

    def test___init__light(self):
        bsa = bsa_files.Fallout4Ba2(self.bsa_path, names_only=True, load_cache=True)
        # print bsa._filenames

if __name__ == '__main__':
    unittest.main()
