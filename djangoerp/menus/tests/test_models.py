#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This file is part of the django ERP project.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

__author__ = 'Emanuele Bertoldi <emanuele.bertoldi@gmail.com>'
__copyright__ = 'Copyright (c) 2013 Emanuele Bertoldi'
__version__ = '0.0.4'

from django.test import TestCase

from ..models import *
    
class MenuTestCase(TestCase):
    def test_unicode_representation(self):
        """Tests Menu's unicode representation.
        """
        m = Menu.objects.create(slug="menu")
        
        self.assertEqual(u"%s" % m, "menu")
        
        m.description = "A test menu."
        
        self.assertEqual(u"%s" % m, "A test menu.")
    
class LinkTestCase(TestCase):
    urls = 'djangoerp.menus.tests.urls'
    
    def setUp(self):
        self.m = Menu.objects.create(slug="menu")
        
    def test_unicode_representation(self):
        """Tests Link's unicode representation.
        """
        l, n = Link.objects.get_or_create(title="Test Link", slug="l", url="/", menu=self.m)
        
        self.assertEqual(u"%s" % l, u"menu | Test Link")
        
        l.title = "Test %(model_name)s"
        l.extra_context = {"model_name": "Connection"}
        
        self.assertEqual(u"%s" % l, u"menu | Test Connection")
        
    def test_plain_absolute_url(self):
        """Tests retrieving a plain Link's absolute URL.
        """
        l1, n = Link.objects.get_or_create(title="Test Link 1", slug="l1", url="/", menu=self.m)
        
        self.assertEqual(l1.get_absolute_url(), "/")
        
    def test_simple_reversing_absolute_url(self):
        """Tests a simple reverse of Link's absolute URL.
        """
        l2, n = Link.objects.get_or_create(title="Test Link 2", slug="l2", url="generic_private_zone_url", menu=self.m)
        
        self.assertEqual(l2.get_absolute_url(), "/private/")
        
    def test_reversing_absolute_url(self):
        """Tests reversing the Link's absolute URL.
        """
        l3, n = Link.objects.get_or_create(title="Test Link 3", slug="l3", url="private_zone_url", context='{"id": "link_url_id_kwarg"}', menu=self.m)
        l3.extra_context = {
            "link_url_id_kwarg": "1",
        }
        
        self.assertEqual(l3.get_absolute_url(), "/private/1")
        
    def test_reversing_complex_absolute_url(self):
        """Tests reversing the Link's absolute URL with complex context lookup.
        """
        l4, n = Link.objects.get_or_create(title="Test Link 4", slug="l4", url="private_zone_url", context='{"id": "object.pk"}', menu=self.m)
        l4.extra_context = {
            "object": {"pk": lambda : 1},
        }
        
        self.assertEqual(l4.get_absolute_url(), "/private/1")
        
    def test_invalid_absolute_url_reversion(self):
        """Tests invalid Link's absolute URL reversion.
        """
        # NOTE: "invalid_private_url" is an invalid URL's name, so there's no valid reversion.
        l5, n = Link.objects.get_or_create(title="Test Link 5", slug="l5", url="invalid_private_url", menu=self.m)
        
        self.assertEqual(l5.get_absolute_url(), "invalid_private_url")
    
class BookmarkTestCase(TestCase):
    def setUp(self):
        self.m = Menu.objects.create(slug="menu")
        self.b = Bookmark.objects.create(title="Test Bookmark", slug="b", url="/", menu=self.m)
        
    def test_unicode_representation(self):
        """Tests Bookmark's unicode representation.
        """
        self.assertEqual(u"%s" % self.b, "Test Bookmark")
        
        self.b.title = "Test %(model_name)s"
        self.b.extra_context = {"model_name": "Connection"}
        
        self.assertEqual(u"%s" % self.b, u"Test Connection")
        
    def test_get_edit_url(self):
        """Tests retrieving the Bookmark's URL for editing.
        """
        self.assertEqual(self.b.get_edit_url(), "/bookmarks/b/edit/")
        
    def test_get_delete_url(self):
        """Tests retrieving the Bookmark's URL for deletion.
        """
        self.assertEqual(self.b.get_delete_url(), "/bookmarks/b/delete/")