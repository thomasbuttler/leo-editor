# -*- coding: utf-8 -*-
#@+leo-ver=5-thin
#@+node:ekr.20210902055206.1: * @file ../unittests/core/test_leoRst3.py
#@@first
"""Tests of leoRst3.py"""
import textwrap
from leo.core import leoGlobals as g
from leo.core.leoTest2 import LeoUnitTest
#@+others
#@+node:ekr.20210327072030.1: ** class TestRst3 (LeoUnitTest)
class TestRst3(LeoUnitTest):
    '''A class to run rst-related unit tests.'''

    #@+others
    #@+node:ekr.20210327072030.3: *3* TestRst3.runLegacyTest (to do)
    def xx_test_legacy_test(self):
        '''run a legacy rst test.'''
        c, p = self.c, self.c.p
        rc = c.rstCommands
        fn = p.h
        source_p = g.findNodeInTree(c, p, 'source')
        # source_s1 = source_p.firstChild().b
        expected_p = g.findNodeInTree(c, p, 'expected')
        expected_source = expected_p.firstChild().b  # type:ignore
        root = source_p.firstChild()  # type:ignore
        rc.http_server_support = True  # Override setting for testing.
        #
        # Compute the result.
        rc.nodeNumber = 0
        source = rc.write_rst_tree(root, fn)
        html = rc.writeToDocutils(p, source, ext='.html')
        #
        # Tests...
        # Don't bother testing the html. It will depend on docutils.
        if 0:
            g.printObj(g.splitLines(source), tag='source')
            g.printObj(g.splitLines(expected_source), tag='expected source')
        self.assertEqual(expected_source, source, msg='expected_s != got_s')
        assert html and html.startswith('<?xml') and html.strip().endswith('</html>')
    #@+node:ekr.20210327092009.1: *3* TestRst3.test_1
    def test_1(self):
        #@+<< define expected_s >>
        #@+node:ekr.20210327092210.1: *4* << define expected_s >>
        expected_s = '''\
        .. rst3: filename: @rst test.html

        .. _http-node-marker-1:

        #####
        Title
        #####

        This is test.html

        .. _http-node-marker-2:

        section
        +++++++

        #@+at This is a doc part
        # it has two lines.
        #@@c
        This is the body of the section.

        '''
        #@-<< define expected_s >>
        c = self.c
        rc = c.rstCommands
        root = c.rootPosition().insertAfter()
        root.h = fn = '@rst test.html'
        #@+<< define root_b >>
        #@+node:ekr.20210327092818.1: *4* << define root_b >>
        root_b = '''\
        #####
        Title
        #####

        This is test.html
        '''
        #@-<< define root_b >>
        root.b = textwrap.dedent(root_b)
        child = root.insertAsLastChild()
        child.h = 'section'
        #@+<< define child_b >>
        #@+node:ekr.20210327093238.1: *4* << define child_b >>
        child_b = '''\
        #@+at This is a doc part
        # it has two lines.
        #@@c
        This is the body of the section.
        '''
        #@-<< define child_b >>
        child.b = textwrap.dedent(child_b)
        expected_source = textwrap.dedent(expected_s)
        #
        # Compute the result.
        rc.nodeNumber = 0
        rc.http_server_support = True  # Override setting for testing.
        source = rc.write_rst_tree(root, fn)
        html = rc.writeToDocutils(root, source, ext='.html')
        #
        # Tests...
        # Don't bother testing the html. It will depend on docutils.
        self.assertEqual(expected_source, source, msg='expected_source != source')
        assert html and html.startswith('<?xml') and html.strip().endswith('</html>')
    #@-others
#@-others
#@-leo
