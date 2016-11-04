import os
import unittest
from collections import OrderedDict
from pprint import pprint
from unittest import TestCase
import sys
from os.path import dirname, abspath, sep

import itertools

import struct

from test_bash.test_bosh.test_bsa_files_constants import Skyrim_Interface_bsa, \
    Oblivion_Misc_bsa, \
    HeartOftheDead_Folder_Names, MidasSpells

mopy = dirname(dirname(dirname(abspath(__file__))))
assert mopy.split(sep)[-1].lower() == 'mopy'
sys.path.insert(0, mopy)
print 'Mopy folder inserted to path: ', mopy
# http://stackoverflow.com/q/40022220/281545
from bash.bosh import bsa_files

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

class TestOblivionBsa(TestCase):
    bsa_path = r'F:\GAMES\TESIV\Oblivion\Data\Oblivion - Misc.bsa'

    def test___init__(self):
        bsa = bsa_files.OblivionBsa(self.bsa_path, names_only=False)
        # pprint(bsa.bsa_folders)
        od = OrderedDict()
        for k, v in bsa.bsa_folders.iteritems():
            od[k] = (tuple(unicode(a) for a in v.assets.itervalues()))
        # pprint(od)
        assert od == Oblivion_Misc_bsa

    def test___init__light(self):
        bsa = bsa_files.OblivionBsa(self.bsa_path, names_only=True)
        assert bsa._filenames == list(
            itertools.chain.from_iterable(Oblivion_Misc_bsa.values()))

class TestHeartOfTheDead(TestCase):
    bsa_path = r'F:\GAMES\TESIV\Oblivion\Data\HeartOftheDead.bsa'
    folder_names = HeartOftheDead_Folder_Names

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

class TestSkyrimBsa(TestCase):
    bsa_path = r'F:\GAMES\Skyrim\Data\Skyrim - Interface.bsa'

    def test___init__(self):
        bsa = bsa_files.SkyrimBsa(self.bsa_path, names_only=False)
        # pprint(bsa.bsa_folders)
        od = OrderedDict()
        for k, v in bsa.bsa_folders.iteritems():
            od[k] = (tuple(unicode(a) for a in v.assets.itervalues()))
        # pprint(od)
        assert od == Skyrim_Interface_bsa

    def test___init__light(self):
        bsa = bsa_files.SkyrimBsa(self.bsa_path, names_only=True)
        assert bsa._filenames == list(
            itertools.chain.from_iterable(Skyrim_Interface_bsa.itervalues()))

class TestFallout4Ba2(TestCase):
    bsa_path = r"F:\GAMES\FALLOUT 4\Data\Fallout4 - Animations.ba2"

    def test___init__(self):
        bsa = bsa_files.Fallout4Ba2(self.bsa_path, names_only=False)
        # pprint(bsa.bsa_folders)
        # od = OrderedDict()
        # for k, v in bsa.bsa_folders.iteritems():
        #     od[k] = (tuple(unicode(a) for a in v.assets.itervalues()))
        # pprint(od)
        # assert od == Skyrim_Interface_bsa

    def test___init__light(self):
        bsa = bsa_files.Fallout4Ba2(self.bsa_path, names_only=True)
        # print bsa._filenames

if __name__ == '__main__':
    unittest.main()
