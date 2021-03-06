#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import re
from lxml import etree
from . import xhtml2odt

class ParagraphElements(unittest.TestCase):

    def test_p1(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p>Test</p></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, """<text:p text:style-name="Text_20_body">Test</text:p>""")

    def test_p_containing_ul(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p><ul><li>Test</li></ul></p></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, """<text:list text:style-name="List_20_1">
  <text:list-item>
    <text:p text:style-name="list-item-bullet">Test</text:p>
  </text:list-item>
</text:list>""")

    def test_p_containing_ol(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p><ol><li>Test</li></ol></p></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, """<text:list text:style-name="Numbering_20_1">
  <text:list-item>
    <text:p text:style-name="list-item-number">Test</text:p>
  </text:list-item>
</text:list>""")

    def test_p_containing_blockquote(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p><blockquote><p>Test</p></blockquote></p></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, """<text:p text:style-name="Quotations">Test</text:p>""")

    def test_p_containing_pre(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p><pre>Test</pre></p></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, """<text:p text:style-name="Preformatted_20_Text">Test</text:p>"""
                               """<text:p text:style-name="Text_20_body"/>""")

    def test_p_containing_dl(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p><dl><dt>Term</dt><dd>Value</dd></dl></p></html>'
        odt = xhtml2odt(html)
        print odt
        self.assertEquals(odt, """<text:p text:style-name="Definition_20_Term">Term</text:p>"""
                               """<text:p text:style-name="Definition_20_Description">Value</text:p>""")

    def test_p_containing_text_and_block(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p>Top text<pre>Test</pre>Bottom text</p></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, """<text:p text:style-name="Text_20_body">Top text</text:p>"""
                               """<text:p text:style-name="Preformatted_20_Text">Test</text:p>"""
                               """<text:p text:style-name="Text_20_body"/>""" # added by the <pre> tag for readability
                               """<text:p text:style-name="Text_20_body">Bottom text</text:p>""")

    def test_p_containing_text_and_inline_and_block(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p>Top <sup>sup text</sup> text<pre>Test</pre></p></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, """<text:p text:style-name="Text_20_body">Top """
                               """<text:span text:style-name="sup">sup text</text:span> text</text:p>"""
                               """<text:p text:style-name="Preformatted_20_Text">Test</text:p>"""
                               """<text:p text:style-name="Text_20_body"/>""")

#    def test_p_containing_text_and_2_blocks(self):
#        # Unsupported yet
#        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p>Top text<pre>Block 1</pre>Middle text<pre>Block 2</pre>Bottom text</p></html>'
#        odt = xhtml2odt(html)
#        print odt
#        assert str(odt) == """<?xml version="1.0" encoding="utf-8"?>
#<text:p text:style-name="Text_20_body">Top text</text:p>""" + \
#"""<text:p text:style-name="Preformatted_20_Text">Block 1</text:p>""" + \
#"""<text:p text:style-name="Text_20_body">Middle text</text:p>""" + \
#"""<text:p text:style-name="Preformatted_20_Text">Block 2</text:p>""" + \
#"""<text:p text:style-name="Text_20_body">Bottom text</text:p>
#"""

    def test_p_containing_text_and_2_inlines(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p>Top text<sup>inline text 1</sup>Middle text<sup>inline text 2</sup>Bottom text<pre>Test</pre></p></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, """<text:p text:style-name="Text_20_body">Top text"""
                               """<text:span text:style-name="sup">inline text 1</text:span>Middle text"""
                               """<text:span text:style-name="sup">inline text 2</text:span>Bottom text</text:p>"""
                               """<text:p text:style-name="Preformatted_20_Text">Test</text:p>"""
                               """<text:p text:style-name="Text_20_body"/>""")

    def test_p_center1(self):
        """<p> tag: with text-align: center (space)"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p style="text-align: center">Test</p></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, """<text:p text:style-name="center">Test</text:p>""")

    def test_p_center2(self):
        """<p> tag: with text-align:center (no space)"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p style="text-align:center">Test</p></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, """<text:p text:style-name="center">Test</text:p>""")

    def test_p_left(self):
        """<p> tag: with text-align: left"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p style="text-align: left">Test</p></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, """<text:p text:style-name="left">Test</text:p>""")

    def test_p_right(self):
        """<p> tag: with text-align: right"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p style="text-align: right">Test</p></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, """<text:p text:style-name="right">Test</text:p>""")

    def test_p_justify(self):
        """<p> tag: with text-align: justify"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p style="text-align: justify">Test</p></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, """<text:p text:style-name="justify">Test</text:p>""")

    def test_p_inside_p(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><table><tr><td><p>Test</p></td></tr></table></html>'
        odt = xhtml2odt(html)
        print odt
        self.assertEquals(str(odt).count("Test"), 1,
            "Paragraphs inside paragraph-like elements should be accepted")

    def test_p_inside_p2(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p><p><img src="test"/></p></p></html>'
        odt = xhtml2odt(html)
        print odt
        self.assertEquals(str(odt).count("<text:p"), 1,
            "Elements inside double-paragraphs must not add their own paragraph wrapper")


if __name__ == '__main__':
    unittest.main()
