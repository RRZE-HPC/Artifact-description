#!/usr/bin/env python3
"""
High-level tests for the class InfoGroup
"""
import os
import sys
import unittest
import tempfile
import shutil
import stat
from machinestate import InfoGroup
from locale import getpreferredencoding

ENCODING = getpreferredencoding()

class TestInfoGroupBase(unittest.TestCase):
    def test_empty(self):
        cls = InfoGroup()
        self.assertEqual(cls.name, None)
        self.assertEqual(cls.extended, False)
        self.assertEqual(cls.anon, False)
        self.assertEqual(cls.files, {})
        self.assertEqual(cls.commands, {})
        self.assertEqual(cls.constants, {})
        self.assertEqual(cls._instances, [])

    def test_named(self):
        cls = InfoGroup(name="Testname")
        self.assertEqual(cls.name, "Testname")
    def test_extended(self):
        cls = InfoGroup(extended=True)
        self.assertEqual(cls.extended, True)
    def test_anon(self):
        cls = InfoGroup(anon=True)
        self.assertEqual(cls.anon, True)
    def test_constant(self):
        testdict = {"Test1" : "Test", "Test2" : "Test", "Test3" : 3}
        cls = InfoGroup()
        cls.constants = testdict
        cls.generate()
        cls.update()
        outdict = cls.get()
        for key in testdict:
            self.assertEqual(testdict[key], outdict[key])

class TestInfoGroupFiles(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.temp_dir = tempfile.mkdtemp()
        self.temp_files = {"File{}".format(x) : tempfile.mkstemp(prefix=str(x), dir=self.temp_dir) for x in range(4)}
        for tkey in self.temp_files:
            tfp, tfname = self.temp_files[tkey]
            os.pwrite(tfp, bytes("{}\n".format(tkey), ENCODING), 0)
            os.close(tfp)

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.temp_dir)

    def test_files(self):
        resdict = {"File{}".format(x) : "File{}".format(x) for x in range(4)}
        cls = InfoGroup()
        for tkey in self.temp_files:
            _, tfname = self.temp_files[tkey]
            cls.files[tkey] = (tfname,)
        cls.generate()
        cls.update()
        outdict = cls.get()
        for i,tkey in enumerate(resdict):
            self.assertEqual(resdict[tkey], outdict[tkey])
    def test_filesmatch(self):
        resdict = {"File{}".format(x) : "{}".format(x) for x in range(4)}
        match = r"File(\d+)"
        cls = InfoGroup()
        for tkey in self.temp_files:
            _, tfname = self.temp_files[tkey]
            cls.files[tkey] = (tfname, match)
        cls.generate()
        cls.update()
        outdict = cls.get()
        for i,tkey in enumerate(resdict):
            self.assertEqual(resdict[tkey], outdict[tkey])
    def test_filesmatchconvert(self):
        resdict = {"File{}".format(x) : x for x in range(4)}
        match = r"File(\d+)"
        cls = InfoGroup()
        for tkey in self.temp_files:
            _, tfname = self.temp_files[tkey]
            cls.files[tkey] = (tfname, match, int)
        cls.generate()
        cls.update()
        outdict = cls.get()
        for i,tkey in enumerate(resdict):
            self.assertEqual(resdict[tkey], outdict[tkey])

class TestInfoGroupCommands(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.temp_dir = tempfile.mkdtemp()
        self.temp_files = {"File{}".format(x) : tempfile.mkstemp(prefix=str(x), dir=self.temp_dir) for x in range(4)}
        for tkey in self.temp_files:
            tfp, tfname = self.temp_files[tkey]
            os.pwrite(tfp, bytes("{}\n".format(tkey), ENCODING), 0)
            os.close(tfp)

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.temp_dir)
    def test_commands(self):
        resdict = {"File{}".format(x) : "File{}".format(x) for x in range(4)}
        cls = InfoGroup()
        for tkey in self.temp_files:
            _, tfname = self.temp_files[tkey]
            cls.commands[tkey] = ("echo", "{}".format(tkey))
        cls.generate()
        cls.update()
        outdict = cls.get()
        for i,tkey in enumerate(resdict):
            self.assertEqual(resdict[tkey], outdict[tkey])
    def test_commandsmatch(self):
        resdict = {"File{}".format(x) : "{}".format(x) for x in range(4)}
        match = r"File(\d+)"
        cls = InfoGroup()
        for tkey in self.temp_files:
            _, tfname = self.temp_files[tkey]
            cls.commands[tkey] = ("echo", "{}".format(tkey), match)
        cls.generate()
        cls.update()
        outdict = cls.get()
        for i,tkey in enumerate(resdict):
            self.assertEqual(resdict[tkey], outdict[tkey])
    def test_commandsmatchconvert(self):
        resdict = {"File{}".format(x) : x for x in range(4)}
        match = r"File(\d+)"
        cls = InfoGroup()
        for tkey in self.temp_files:
            _, tfname = self.temp_files[tkey]
            cls.commands[tkey] = ("echo", "{}".format(tkey), match, int)
        cls.generate()
        cls.update()
        outdict = cls.get()
        for i,tkey in enumerate(resdict):
            self.assertEqual(resdict[tkey], outdict[tkey])