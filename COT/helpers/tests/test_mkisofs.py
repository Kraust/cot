#!/usr/bin/env python
# coding=utf-8
#
# test_mkisofs.py - Unit test cases for COT.helpers.mkisofs submodule.
#
# March 2015, Glenn F. Matthews
# Copyright (c) 2014-2016 the COT project developers.
# See the COPYRIGHT.txt file at the top-level directory of this distribution
# and at https://github.com/glennmatthews/cot/blob/master/COPYRIGHT.txt.
#
# This file is part of the Common OVF Tool (COT) project.
# It is subject to the license terms in the LICENSE.txt file found in the
# top-level directory of this distribution and at
# https://github.com/glennmatthews/cot/blob/master/LICENSE.txt. No part
# of COT, including this file, may be copied, modified, propagated, or
# distributed except according to the terms contained in the LICENSE.txt file.

"""Unit test cases for the COT.helpers.mkisofs submodule."""

from distutils.version import StrictVersion
import mock

from COT.helpers.tests.test_helper import HelperUT
from COT.helpers.helper import Helper
from COT.helpers.mkisofs import MkIsoFS


class TestMkIsoFS(HelperUT):
    """Test cases for MkIsoFS helper class."""

    def setUp(self):
        """Test case setup function called automatically prior to each test."""
        self.helper = MkIsoFS()
        super(TestMkIsoFS, self).setUp()

    @mock.patch('COT.helpers.helper.Helper._check_output',
                return_value=("mkisofs 3.00 (--) Copyright (C) 1993-1997 "
                              "Eric Youngdale (C) 1997-2010 Jörg Schilling"))
    def test_get_version_mkisofs(self, _):
        """Test .version getter logic for mkisofs."""
        self.assertEqual(StrictVersion("3.0"), self.helper.version)

    @mock.patch('COT.helpers.helper.Helper._check_output',
                return_value="genisoimage 1.1.11 (Linux)")
    def test_get_version_genisoimage(self, _):
        """Test .version getter logic for genisoimage."""
        self.assertEqual(StrictVersion("1.1.11"), self.helper.version)

    @mock.patch('COT.helpers.helper.Helper.find_executable')
    def test_find_mkisofs(self, mock_find_executable):
        """If mkisofs is found, use it."""
        def find_one(name):
            """Find mkisofs but no other."""
            if name == "mkisofs":
                return "/mkisofs"
            return None
        mock_find_executable.side_effect = find_one
        self.assertEqual("mkisofs", self.helper.name)
        self.assertEqual(self.helper.path, "/mkisofs")

    @mock.patch('COT.helpers.helper.Helper.find_executable')
    def test_find_genisoimage(self, mock_find_executable):
        """If mkisofs is not found, but genisoimage is, use that."""
        def find_one(name):
            """Find genisoimage but no other."""
            if name == "genisoimage":
                return "/genisoimage"
            return None
        mock_find_executable.side_effect = find_one
        self.assertEqual("genisoimage", self.helper.name)
        self.assertEqual(self.helper.path, "/genisoimage")

    @mock.patch('COT.helpers.helper.Helper._check_output')
    @mock.patch('subprocess.check_call')
    def test_install_helper_already_present(self, mock_check_call,
                                            mock_check_output):
        """Don't re-install if already installed."""
        self.helper.install_helper()
        mock_check_output.assert_not_called()
        mock_check_call.assert_not_called()
        self.assertLogged(**self.ALREADY_INSTALLED)

    def test_install_helper_port(self):
        """Test installation via 'port'."""
        self.port_install_test('cdrtools')

    def test_install_helper_apt_get(self):
        """Test installation via 'apt-get'."""
        self.apt_install_test('genisoimage', 'genisoimage')
