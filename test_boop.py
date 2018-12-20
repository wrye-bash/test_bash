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
import os
import shutil
import tempfile
import unittest
from xml.etree import ElementTree as etree

import boop


class MimicChainMap(object):
    def __init__(self):
        self.maps = []


class TestGetInstallerFiles(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_empty(self):
        with self.assertRaises(IOError):
            boop._get_installer_files(self.tmpdir)

    def test_missing_fomod_folder(self):
        fake_path = os.path.join(self.tmpdir, 'fomod')
        with self.assertRaises(IOError):
            boop._get_installer_files(fake_path)

    def test_missing_config(self):
        os.makedirs(os.path.join(self.tmpdir, 'fomod'))
        open(os.path.join(self.tmpdir, 'fomod', 'info.xml'), 'a').close()
        with self.assertRaises(IOError):
            boop._get_installer_files(self.tmpdir)

    def test_missing_info(self):
        os.makedirs(os.path.join(self.tmpdir, 'fomod'))
        conf_path = os.path.join(self.tmpdir, 'fomod', 'ModuleConfig.xml')
        open(conf_path, 'a').close()
        with self.assertRaises(IOError):
            boop._get_installer_files(self.tmpdir)

    def test_valid(self):
        fomod_path = os.path.join(self.tmpdir, 'fomod')
        info_file = os.path.join(fomod_path, 'info.xml')
        conf_file = os.path.join(fomod_path, 'ModuleConfig.xml')
        os.makedirs(fomod_path)
        open(info_file, 'a').close()
        open(conf_file, 'a').close()
        expected = (info_file, conf_file)
        self.assertEqual(boop._get_installer_files(self.tmpdir), expected)
        self.assertEqual(boop._get_installer_files(fomod_path), expected)


class TestAssertDependencies(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_ok_flag_states(self):
        depend = etree.fromstring('<dependencies operator="And">'
                                  '<flagDependency flag="a" value="on"/>'
                                  '</dependencies>')
        flag_states = {'a': 'on'}
        boop._assert_dependencies(depend, flag_states)

    def test_missing_flag_states(self):
        depend = etree.fromstring('<dependencies operator="And">'
                                  '<flagDependency flag="a" value="on"/>'
                                  '</dependencies>')
        flag_states = {}
        with self.assertRaises(boop.MissingDependency):
            boop._assert_dependencies(depend, flag_states)

    def test_fail_flag_states(self):
        depend = etree.fromstring('<dependencies operator="And">'
                                  '<flagDependency flag="a" value="on"/>'
                                  '</dependencies>')
        flag_states = {'a': 'off'}
        with self.assertRaises(boop.MissingDependency):
            boop._assert_dependencies(depend, flag_states)

    def test_ok_active_file_depend(self):
        open(os.path.join(self.tmpdir, 'test_file'), 'a').close()
        depend = etree.fromstring('<dependencies operator="And">'
                                  '<fileDependency file="test_file" '
                                  'state="Active"/>'
                                  '</dependencies>')
        boop._assert_dependencies(depend, {}, self.tmpdir)

    def test_fail_active_file_depend(self):
        depend = etree.fromstring('<dependencies operator="And">'
                                  '<fileDependency file="test_file" '
                                  'state="Active"/>'
                                  '</dependencies>')
        with self.assertRaises(boop.MissingDependency):
            boop._assert_dependencies(depend, {}, self.tmpdir)

    def test_ok_missing_file_depend(self):
        depend = etree.fromstring('<dependencies operator="And">'
                                  '<fileDependency file="test_file" '
                                  'state="Missing"/>'
                                  '</dependencies>')
        boop._assert_dependencies(depend, {}, self.tmpdir)

    def test_fail_missing_file_depend(self):
        open(os.path.join(self.tmpdir, 'test_file'), 'a').close()
        depend = etree.fromstring('<dependencies operator="And">'
                                  '<fileDependency file="test_file" '
                                  'state="Missing"/>'
                                  '</dependencies>')
        with self.assertRaises(boop.MissingDependency):
            boop._assert_dependencies(depend, {}, self.tmpdir)

    def test_ok_game_version(self):
        depend = etree.fromstring('<dependencies operator="And">'
                                  '<gameDependency version="1.0.1"/>'
                                  '</dependencies>')
        boop._assert_dependencies(depend, {}, game_version='1.2')

    def test_fail_game_version(self):
        depend = etree.fromstring('<dependencies operator="And">'
                                  '<gameDependency version="1.0.1"/>'
                                  '</dependencies>')
        with self.assertRaises(boop.MissingDependency):
            boop._assert_dependencies(depend, {}, game_version='1.0')

    def test_nested_fail(self):
        depend = etree.fromstring('<dependencies operator="And">'
                                  '<dependencies>'
                                  '<flagDependency flag="a" value="on"/>'
                                  '</dependencies>'
                                  '</dependencies>')
        flag_states = {}
        with self.assertRaises(boop.MissingDependency):
            boop._assert_dependencies(depend, flag_states)

    def test_fail_or_operator(self):
        depend = etree.fromstring('<dependencies operator="Or">'
                                  '<gameDependency version="1.0.1"/>'
                                  '<flagDependency flag="a" value="on"/>'
                                  '</dependencies>')
        with self.assertRaises(boop.MissingDependency):
            boop._assert_dependencies(depend, {}, game_version='1.0')


class TestCollectFiles(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.file_list = etree.fromstring('<requiredInstallFiles>'
                                          '<file source="example.plugin"/>'
                                          '<folder source="example_folder"/>'
                                          '</requiredInstallFiles>')

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def runTest(self):
        test_chain = MimicChainMap()
        expected = [{'0': {'example_folder': '', 'example.plugin': ''}}]
        boop._collect_files(self.file_list, test_chain)
        self.assertEqual(test_chain.maps, expected)


class TestCollectFlags(unittest.TestCase):
    def runTest(self):
        flag_states = MimicChainMap()
        flag_list = etree.fromstring('<conditionFlags>'
                                     '<flag name="a">on</flag>'
                                     '<flag name="b">off</flag>'
                                     '<flag name="c"/>'
                                     '</conditionFlags>')
        expected = [{'a': 'on', 'b': 'off', 'c': ''}]
        boop._collect_flags(flag_list, flag_states)
        self.assertEqual(flag_states.maps, expected)


class TestExplicitList(unittest.TestCase):
    def test_none(self):
        self.assertEqual(boop._explicit_list(None), [])

    def test_real_list(self):
        root = etree.fromstring('<patterns>'
                                '<pattern/>'
                                '<pattern/>'
                                '<pattern/>'
                                '<pattern/>'
                                '<pattern/>'
                                '</patterns>')
        self.assertEqual(boop._explicit_list(root), list(root))


class TestOrderedList(unittest.TestCase):
    def test_none(self):
        self.assertEqual(boop._ordered_list(None), [])

    def test_ascending(self):
        root = etree.fromstring('<installSteps order="Ascending">'
                                '<installStep name="A"/>'
                                '<installStep name="C"/>'
                                '<installStep name="B"/>'
                                '</installSteps>')
        expected = [root[0], root[2], root[1]]
        self.assertEqual(boop._ordered_list(root), expected)

    def test_descending(self):
        root = etree.fromstring('<installSteps order="Descending">'
                                '<installStep name="A"/>'
                                '<installStep name="C"/>'
                                '<installStep name="B"/>'
                                '</installSteps>')
        expected = [root[1], root[2], root[0]]
        self.assertEqual(boop._ordered_list(root), expected)

    def test_explicit(self):
        root = etree.fromstring('<installSteps order="Explicit">'
                                '<installStep name="A"/>'
                                '<installStep name="C"/>'
                                '<installStep name="B"/>'
                                '</installSteps>')
        expected = [root[0], root[1], root[2]]
        self.assertEqual(boop._ordered_list(root), expected)


class TestInstaller(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def runTest(self):
        source_dir = os.path.join(self.tmpdir, 'source')
        target_dir = os.path.join(self.tmpdir, 'target')
        os.makedirs(source_dir)
        os.makedirs(target_dir)

        info_xml = ('<fomod>'
                    '<Name>Test Mod</Name>'
                    '<Author>Test Author</Author>'
                    '<Version>1.0.0</Version>'
                    '<Description>Test description.</Description>'
                    '<Website>www.test.org</Website>'
                    '</fomod>')
        conf_xml = ('<config xmlns:xsi="http://www.w3.org/2001/'
                    'XMLSchema-instance" xsi:noNamespaceSchemaL'
                    'ocation="http://qconsulting.ca/fo3/ModConfig5.0.xsd">'
                    '<moduleName>Test Mod</moduleName>'
                    '<moduleImage path="test_image.png"/>'
                    '<moduleDependencies operator="And">'
                    '<fileDependency file="depend1.plugin" state="Missing"/>'
                    '<dependencies operator="Or">'
                    '<fileDependency file="depend2v1.plugin" state="Active"/>'
                    '<fileDependency file="depend2v2.plugin" state="Active"/>'
                    '</dependencies>'
                    '</moduleDependencies>'
                    '<requiredInstallFiles>'
                    '<file source="test.plugin"/>'
                    '</requiredInstallFiles>'
                    '<installSteps order="Explicit">'
                    '<installStep name="First Step">'
                    '<optionalFileGroups order="Explicit">'
                    '<group name="First Option:" type="SelectExactlyOne">'
                    '<plugins order="Explicit">'
                    '<plugin name="Option 01">'
                    '<description>Select this to '
                    'install Option 01.</description>'
                    '<image path="option_01.png"/>'
                    '<conditionFlags>'
                    '<flag name="option_01">selected</flag>'
                    '</conditionFlags>'
                    '<typeDescriptor>'
                    '<type name="Recommended"/>'
                    '</typeDescriptor>'
                    '</plugin>'
                    '<plugin name="Option 02">'
                    '<description>Select this to '
                    'install Option 02.</description>'
                    '<image path="option_02.png"/>'
                    '<conditionFlags>'
                    '<flag name="option_02">selected</flag>'
                    '</conditionFlags>'
                    '<typeDescriptor>'
                    '<type name="Optional"/>'
                    '</typeDescriptor>'
                    '</plugin>'
                    '</plugins>'
                    '</group>'
                    '<group name="Mandatory Option:" type="SelectAll">'
                    '<plugins order="Explicit">'
                    '<plugin name="Option 03">'
                    '<description>Option 03 is '
                    'required by group.</description>'
                    '<image path="option_03.png"/>'
                    '<files>'
                    '<folder source="option_03"/>'
                    '</files>'
                    '<typeDescriptor>'
                    '<type name="Required"/>'
                    '</typeDescriptor>'
                    '</plugin>'
                    '</plugins>'
                    '</group>'
                    '</optionalFileGroups>'
                    '</installStep>'
                    '<installStep name="Second Step 01">'
                    '<visible>'
                    '<flagDependency flag="option_01" value="selected"/>'
                    '</visible>'
                    '<optionalFileGroups order="Explicit">'
                    '<group name="First Option:" type="SelectExactlyOne">'
                    '<plugins order="Explicit">'
                    '<plugin name="Option 11">'
                    '<description>Select this to '
                    'install Option 11.</description>'
                    '<image path="option_11.png"/>'
                    '<conditionFlags>'
                    '<flag name="option_11">selected</flag>'
                    '</conditionFlags>'
                    '<typeDescriptor>'
                    '<type name="Optional"/>'
                    '</typeDescriptor>'
                    '</plugin>'
                    '<plugin name="Option 21">'
                    '<description>Select this to '
                    'install Option 21.</description>'
                    '<image path="option_21.png"/>'
                    '<conditionFlags>'
                    '<flag name="option_21">selected</flag>'
                    '</conditionFlags>'
                    '<typeDescriptor>'
                    '<type name="Required"/>'
                    '</typeDescriptor>'
                    '</plugin>'
                    '</plugins>'
                    '</group>'
                    '</optionalFileGroups>'
                    '</installStep>'
                    '<installStep name="Second Step 02">'
                    '<visible>'
                    '<flagDependency flag="option_02" value="selected"/>'
                    '</visible>'
                    '<optionalFileGroups order="Explicit">'
                    '<group name="First Option:" type="SelectExactlyOne">'
                    '<plugins order="Explicit">'
                    '<plugin name="Option 12">'
                    '<description>Select this to '
                    'install Option 12.</description>'
                    '<image path="option_12.png"/>'
                    '<conditionFlags>'
                    '<flag name="option_12">selected</flag>'
                    '</conditionFlags>'
                    '<typeDescriptor>'
                    '<type name="Optional"/>'
                    '</typeDescriptor>'
                    '</plugin>'
                    '</plugins>'
                    '</group>'
                    '</optionalFileGroups>'
                    '</installStep>'
                    '<installStep name="Third Step">'
                    '<optionalFileGroups order="Explicit">'
                    '<group name="First Option:" type="SelectAtMostOne">'
                    '<plugins order="Explicit">'
                    '<plugin name="Option 3">'
                    '<description>Select this to '
                    'install Option 3.</description>'
                    '<files>'
                    '<file source="option_3.plugin"/>'
                    '</files>'
                    '<typeDescriptor>'
                    '<dependencyType>'
                    '<defaultType name="Optional"/>'
                    '<patterns>'
                    '<pattern>'
                    '<dependencies operator="And">'
                    '<flagDependency flag="option_02" value="selected"/>'
                    '</dependencies>'
                    '<type name="Optional"/>'
                    '</pattern>'
                    '<pattern>'
                    '<dependencies operator="And">'
                    '<flagDependency flag="option_01" value="selected"/>'
                    '</dependencies>'
                    '<type name="NotUsable"/>'
                    '</pattern>'
                    '</patterns>'
                    '</dependencyType>'
                    '</typeDescriptor>'
                    '</plugin>'
                    '</plugins>'
                    '</group>'
                    '</optionalFileGroups>'
                    '</installStep>'
                    '</installSteps>'
                    '<conditionalFileInstalls>'
                    '<patterns>'
                    '<pattern>'
                    '<dependencies operator="And">'
                    '<flagDependency flag="option_11" value="selected"/>'
                    '</dependencies>'
                    '<files>'
                    '<file source="option_11"/>'
                    '</files>'
                    '</pattern>'
                    '<pattern>'
                    '<dependencies operator="And">'
                    '<flagDependency flag="option_12" value="selected"/>'
                    '</dependencies>'
                    '<files>'
                    '<file source="option_12"/>'
                    '</files>'
                    '</pattern>'
                    '<pattern>'
                    '<dependencies operator="And">'
                    '<flagDependency flag="option_21" value="selected"/>'
                    '</dependencies>'
                    '<files>'
                    '<file source="option_21"/>'
                    '</files>'
                    '</pattern>'
                    '</patterns>'
                    '</conditionalFileInstalls>'
                    '</config>')
        info_file = os.path.join(source_dir, 'info.xml')
        conf_file = os.path.join(source_dir, 'ModuleConfig.xml')
        with open(info_file, 'w') as info_open:
            info_open.write(info_xml)
        with open(conf_file, 'w') as conf_open:
            conf_open.write(conf_xml)

        install = boop.Installer([info_file, conf_file], target_dir)
        self.assertEqual(install.name, "Test Mod")
        self.assertEqual(install.author, "Test Author")
        self.assertEqual(install.version, "1.0.0")
        self.assertEqual(install.description, "Test description.")
        self.assertEqual(install.website, "www.test.org")
        self.assertEqual(install.image, "test_image.png")
        with self.assertRaises(boop.MissingDependency):
            install.send(None)

        open(os.path.join(target_dir, 'depend2v1.plugin'), 'a').close()

        install = boop.Installer([info_file, conf_file], target_dir)
        install.send(None)
        self.assertEqual(install._flag_states.maps, [{}])
        self.assertEqual(install._collected_files.maps,
                         [{'0': {'test.plugin': ''}}, {}])

        # simulate loops with next()
        first_step = next(install)
        # need to compare dicts this way because id is random
        self.assertEqual(first_step['name'], 'First Step')
        group0 = first_step['groups'][0]
        self.assertEqual(group0['name'], 'First Option:')
        self.assertEqual(group0['type'], 'SelectExactlyOne')
        plugin00 = group0['plugins'][0]
        self.assertEqual(plugin00['name'], 'Option 01')
        self.assertEqual(plugin00['description'],
                         'Select this to install Option 01.')
        self.assertEqual(plugin00['image'], 'option_01.png')
        self.assertEqual(plugin00['type'], 'Recommended')
        plugin01 = group0['plugins'][1]
        self.assertEqual(plugin01['name'], 'Option 02')
        self.assertEqual(plugin01['description'],
                         'Select this to install Option 02.')
        self.assertEqual(plugin01['image'], 'option_02.png')
        self.assertEqual(plugin01['type'], 'Optional')
        group1 = first_step['groups'][1]
        self.assertEqual(group1['name'], 'Mandatory Option:')
        self.assertEqual(group1['type'], 'SelectAll')
        plugin10 = group1['plugins'][0]
        self.assertEqual(plugin10['name'], 'Option 03')
        self.assertEqual(plugin10['description'],
                         'Option 03 is required by group.')
        self.assertEqual(plugin10['image'], 'option_03.png')
        self.assertEqual(plugin10['type'], 'Required')

        first_answer = {group0['id']: [plugin01['id']]}
        install.send(first_answer)

        second_step = next(install)
        self.assertEqual(install._flag_states.maps,
                         [{'option_02': 'selected'}, {}])
        self.assertEqual(install._collected_files.maps,
                         [{'0': {'option_03': ''}},
                          {'0': {'test.plugin': ''}},
                          {}])
        self.assertEqual(second_step['name'], 'Second Step 02')
        group0 = second_step['groups'][0]
        self.assertEqual(group0['name'], 'First Option:')
        self.assertEqual(group0['type'], 'SelectExactlyOne')
        plugin00 = group0['plugins'][0]
        self.assertEqual(plugin00['name'], 'Option 12')
        self.assertEqual(plugin00['description'],
                         'Select this to install Option 12.')
        self.assertEqual(plugin00['image'], 'option_12.png')
        self.assertEqual(plugin00['type'], 'Optional')

        second_answer = {'previous_step': True}
        install.send(second_answer)

        # this should be the same as the first step with regened id's
        back_step = next(install)
        self.assertEqual(install._flag_states.maps, [{}])
        self.assertEqual(install._collected_files.maps,
                         [{'0': {'test.plugin': ''}}, {}])
        self.assertEqual(back_step['name'], 'First Step')
        group0 = back_step['groups'][0]
        self.assertEqual(group0['name'], 'First Option:')
        self.assertEqual(group0['type'], 'SelectExactlyOne')
        plugin00 = group0['plugins'][0]
        self.assertEqual(plugin00['name'], 'Option 01')
        self.assertEqual(plugin00['description'],
                         'Select this to install Option 01.')
        self.assertEqual(plugin00['image'], 'option_01.png')
        self.assertEqual(plugin00['type'], 'Recommended')
        plugin01 = group0['plugins'][1]
        self.assertEqual(plugin01['name'], 'Option 02')
        self.assertEqual(plugin01['description'],
                         'Select this to install Option 02.')
        self.assertEqual(plugin01['image'], 'option_02.png')
        self.assertEqual(plugin01['type'], 'Optional')
        group1 = back_step['groups'][1]
        self.assertEqual(group1['name'], 'Mandatory Option:')
        self.assertEqual(group1['type'], 'SelectAll')
        plugin10 = group1['plugins'][0]
        self.assertEqual(plugin10['name'], 'Option 03')
        self.assertEqual(plugin10['description'],
                         'Option 03 is required by group.')
        self.assertEqual(plugin10['image'], 'option_03.png')
        self.assertEqual(plugin10['type'], 'Required')

        back_answer = {group0['id']: [plugin00['id']]}
        install.send(back_answer)

        new_sec_step = next(install)
        self.assertEqual(install._flag_states.maps,
                         [{'option_01': 'selected'}, {}])
        self.assertEqual(install._collected_files.maps,
                         [{'0': {'option_03': ''}},
                          {'0': {'test.plugin': ''}},
                          {}])
        self.assertEqual(new_sec_step['name'], 'Second Step 01')
        group0 = new_sec_step['groups'][0]
        self.assertEqual(group0['name'], 'First Option:')
        self.assertEqual(group0['type'], 'SelectExactlyOne')
        plugin00 = group0['plugins'][0]
        self.assertEqual(plugin00['name'], 'Option 11')
        self.assertEqual(plugin00['description'],
                         'Select this to install Option 11.')
        self.assertEqual(plugin00['image'], 'option_11.png')
        self.assertEqual(plugin00['type'], 'Optional')
        plugin01 = group0['plugins'][1]
        self.assertEqual(plugin01['name'], 'Option 21')
        self.assertEqual(plugin01['description'],
                         'Select this to install Option 21.')
        self.assertEqual(plugin01['image'], 'option_21.png')
        self.assertEqual(plugin01['type'], 'Required')

        new_sec_answer = {group0['id']: [plugin00['id']]}
        install.send(new_sec_answer)

        third_step = next(install)
        self.assertEqual(install._flag_states.maps,
                         [{'option_11': 'selected', 'option_21': 'selected'},
                          {'option_01': 'selected'},
                          {}])
        self.assertEqual(install._collected_files.maps,
                         [{}, {'0': {'option_03': ''}},
                          {'0': {'test.plugin': ''}}, {}])
        self.assertEqual(third_step['name'], 'Third Step')
        group0 = third_step['groups'][0]
        self.assertEqual(group0['name'], 'First Option:')
        self.assertEqual(group0['type'], 'SelectAtMostOne')
        plugin00 = group0['plugins'][0]
        self.assertEqual(plugin00['name'], 'Option 3')
        self.assertEqual(plugin00['description'],
                         'Select this to install Option 3.')
        self.assertEqual(plugin00['image'], '')
        self.assertEqual(plugin00['type'], 'NotUsable')

        third_answer = {}
        install.send(third_answer)

        with self.assertRaises(StopIteration):
            next(install)
        self.assertEqual(install._flag_states.maps,
                         [{},
                          {'option_11': 'selected', 'option_21': 'selected'},
                          {'option_01': 'selected'},
                          {}])
        self.assertEqual(install._collected_files.maps,
                         [{'0': {'option_21': ''}},
                          {'0': {'option_11': ''}},
                          {},
                          {},
                          {'0': {'option_03': ''}},
                          {'0': {'test.plugin': ''}},
                          {}])
        self.assertEqual(install.flag_states,
                         {'option_01': 'selected',
                          'option_11': 'selected',
                          'option_21': 'selected'})
        self.assertEqual(install.collected_files,
                         {'option_03': '',
                          'option_11': '',
                          'option_21': '',
                          'test.plugin': ''})
