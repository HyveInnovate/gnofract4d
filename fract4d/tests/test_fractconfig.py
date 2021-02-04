#!/usr/bin/env python3

# test configuration file parsing

import os.path

from . import testbase

from fract4d import fractconfig


class Test(testbase.TestSetup):
    def testCreate(self):
        c = self.userConfig

    def testGetDefaults(self):
        c = self.userConfig
        self.assertEqual("gcc", c.get("compiler", "name"))

    def testGetList(self):
        c = fractconfig.T("")
        l = c.get_list("map_path")
        self.assertEqual(4, len(l))
        self.assertEqual("maps", l[0])

    def testSetList(self):
        c = self.userConfig
        l = ["fish"]

        c.set_list("map_path", l)

        l2 = c.get_list("map_path")
        self.assertEqual(l, l2)

    def testSetSize(self):
        c = self.userConfig
        c.set_size(871, 313)
        self.assertEqual(871, c.getint("display", "width"))
        self.assertEqual(313, c.getint("display", "height"))

    def testSetSizeToSameNoChangeSignal(self):
        c = self.userConfig
        c.set_size(871, 313)
        c.changed = self.assertNotCalled
        c.set_size(871, 313)

    def assertNotCalled(self, *args):
        self.assertFalse("Should not be called")

    def testSave(self):
        testprefs = os.path.join(self.tmpdir.name, "testprefs")
        c = fractconfig.T(testprefs)
        c.set("general", "cache_dir", os.path.join(self.tmpdir.name,
                                                   "gnofract4d-cache"))
        c.set("compiler", "options", "-foo")
        self.assertEqual("-foo", c.get("compiler", "options"))
        c.save()

        c.set("compiler", "options", "wibble")
        config2 = fractconfig.T(testprefs)  # re-read
        self.assertEqual("-foo", config2.get("compiler", "options"))

    def testInit(self):
        dummy = fractconfig.T(".gnofract4d")
        self.assertEqual(".gnofract4d", os.path.basename(dummy.file))

    def testDataDir(self):
        c = self.userConfig
        datadir = c.get("general", "data_dir")
        self.assertEqual(
            os.path.expandvars("${HOME}/gnofract4d"), datadir)

    def testDarwin(self):
        c = fractconfig.DarwinConfig("testprefs")
        self.assertEqual("open -e", c.get_default_editor())

    def testUpdatePaths(self):
        self.userConfig["formula_path"] = {
            "0": "formulas", "1": "/usr/share/gnofract4d", "2":"/home/fract4d/formulas"}
        self.userConfig.update_paths("formula_path")
        self.assertEqual(
            self.userConfig["formula_path"],
            {"formulas": None, "/usr/share/gnofract4d": None, "/home/fract4d/formulas": None})
