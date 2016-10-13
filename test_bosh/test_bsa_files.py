import unittest
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
print 'top_package',  __name__.split('.')[0]
print __name__
# http://stackoverflow.com/q/40022220/281545
from bash.bosh import bsa_files

class TestBSAHeader(TestCase):
    def test_read_header(self):
        with open('F:\GAMES\TESIV\Oblivion\Data\Oblivion - Misc.bsa',
                  'r') as bsa:
            h = bsa_files.BSAHeader()
            h.read_header(bsa)
            assert h.file_id == 4281154
            assert h.version == 103
            assert h.folder_record_offset == 36
            assert h.archive_flags == 1795
            assert h.folder_count == 10
            assert h.file_count == 115
            assert h.total_folder_name_length == 114
            assert h.total_file_name_length == 2084
            assert h.file_flags == 420

if __name__ == '__main__':
    # from os import sys, path
    # sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
    unittest.main()
