# Copyright (c) 2007 Infrae. All rights reserved.
# See also LICENSE.txt
# SilvaForum
# Python

import SilvaTestCase
from Testing.ZopeTestCase import utils
from zope.component import getMultiAdapter
from datetime import datetime
from DateTime.DateTime import DateTime
import os

test_path = os.path.dirname(__file__)

class ForumTest(SilvaTestCase.SilvaTestCase):
    def afterSetUp(self):
        self.forum = self.addObject(self.getRoot(), 'Forum', 'forum',
                                    title='Forum', product='SilvaForum')
    
    def test_threads(self):
        self.assertEquals(0, len(self.forum.threads()))
        
        self.thread1 = self.addObject(self.forum, 'Thread', 'thread1',
                                      title='Thread 1', product='SilvaForum')
        self.assertEquals(1, len(self.forum.threads()))
    
    def test_add_thread(self):
        # see if the forum is empty like we expect
        self.assertEquals(0,
                len(self.forum.objectValues('Silva Forum Thread')))

        # use our method to add a thread
        newthread = self.forum.add_thread('Topic', 'topic text')

        # see if the thread has been added properly
        self.assertEquals(1,
                len(self.forum.objectValues('Silva Forum Thread')))

        # also see if the thing returned is what we expect it is
        self.assertEquals('Silva Forum Thread', newthread.meta_type)
        self.assertEquals(getattr(self.forum, newthread.id).absolute_url(),
                          newthread.absolute_url())
        self.assertEquals('topic text', newthread.get_text())
        
        # test id uniqueness
        thread1 = self.forum.add_thread('this is title one', 'foo')
        thread2 = self.forum.add_thread('this is title one', 'foo')
        self.assertNotEquals(thread1.id, thread2.id)

    def test_generate_thread_id(self):
        #from Products.SilvaForum.content import _generate_thread_id
        
        # test that the mangle is underscoring
        test_id = 'testing_this_id_one'
        gen_id = self.forum._generate_thread_id('testing this id one')
        self.assertEquals(gen_id, test_id)

        # test special characters in the thread
        # needs special attention, test_forum.py needs to be able
        # to handle bytes and i need to find out how to convert
        # bytes back to normal
        #test_id = 'test this thread for umlaut'
        #gen_id = self.forum._generate_thread_id('test this thread for umlaut')
        #self.assertEquals(gen_id, test_id)
        
        # test valid id's
        #thread = self.forum.add_thread('title', 'blah')
        #self.assertEquals(thread.id, '')
        
        # test repeat id's
        thread1 = self.forum.add_thread('title ', 'blah1')
        thread2 = self.forum.add_thread('title ', 'blah2')
        self.assertNotEquals(thread1.id, thread2.id)
       
        # test numeric repeat id
        thread1 = self.forum.add_thread('2007', 'blah1')
        thread2 = self.forum.add_thread('2007', 'blah2')
        self.assertNotEquals(thread1.id, thread2.id)
        
        # rare repeat case
        thread1 = self.forum.add_thread('happy__2007', 'blah1')
        thread2 = self.forum.add_thread('happy__2007', 'blah2')
        self.assertNotEquals(thread1.id, thread2.id)
        
        # rarer repeat case
        thread1 = self.forum.add_thread('happy  2007', 'blah1')
        thread2 = self.forum.add_thread('happy  2007', 'blah2')
        self.assertNotEquals(thread1.id, thread2.id)

        # test string length
        gen_id = self.forum._generate_thread_id('0000000000 0000000000 0000000000')
        self.assertEquals(gen_id, '0000000000_000000000')

        gen_id = self.forum._generate_thread_id('0000000000')
        self.assertEquals(gen_id, '0000000000')

        # test that the id being generated is an underscored thread
        # and unique
        newthread = self.forum.add_thread('Topic test id', 'topic text too')
        self.assertEquals('Topic_test_id', newthread.id)

        # test reserved ids
        test_id = 'Members'
        gen_id = self.forum._generate_thread_id('Members')
        self.assertEquals(gen_id, test_id)

class ThreadTest(SilvaTestCase.SilvaTestCase):
    def afterSetUp(self):
        self.forum = self.addObject(self.getRoot(), 'Forum', 'forum',
                                    title='Forum', product='SilvaForum')
        self.thread = self.addObject(self.forum, 'Thread', 'thread',
                                     title='Thread', product='SilvaForum')
    
    def test_comments(self):
        self.assertEquals(0, len(self.thread.comments()))
        
        self.comment1 = self.addObject(self.thread, 'Comment', 'comment1',
                                       title='Comment 1', product='SilvaForum')
        self.assertEquals(1, len(self.thread.comments()))
    
    def test_add_comment(self):
        # test if the forum is empty
        self.assertEquals(0,
                len(self.forum.objectValues('Silva Forum Comment')))

        # test add_comment method
        newcomment = self.thread.add_comment('Comment', 'comment text')
        
        # see if the comment has been added properly
        self.assertEquals(1,
                len(self.thread.objectValues('Silva Forum Comment')))
    
    def test_generate_comment_id(self):
        comment = self.thread.add_comment('', 'comment text')
        self.assertEquals(comment.id, 'comment_text')

        comment = self.thread.add_comment('Title', '')
        self.assertEquals(comment.id, 'Title')
        
        # test id generation
        test_id = 'the_comment_id'
        gen_id = self.thread._generate_comment_id('the comment id')
        self.assertEquals(gen_id, test_id)
        
        # test valid id's
        #comment = self.thread.add_comment('title', 'blah1')
        #self.assertNotEquals(comment.id, '')
       
        # test numeric repeat id
        comment1 = self.thread.add_comment('2007', 'blah1')
        comment2 = self.thread.add_comment('2007', 'blah2')
        self.assertNotEquals(comment1.id, comment2.id)
        
        # rare repeat case
        comment1 = self.thread.add_comment('happy__2007', 'blah1')
        comment2 = self.thread.add_comment('happy__2007', 'blah2')
        self.assertNotEquals(comment1.id, comment2.id)
        
        # rarer repeat case
        comment1 = self.thread.add_comment('happy  2007', 'blah1')
        comment2 = self.thread.add_comment('happy  2007', 'blah2')
        self.assertNotEquals(comment1.id, comment2.id)

        gen_id = self.thread._generate_comment_id('0000000000 0000000000 00')
        self.assertEquals(gen_id, '0000000000_000000000')

        gen_id = self.thread._generate_comment_id('0000000000')
        self.assertEquals(gen_id, '0000000000')

class ThreadViewTest(SilvaTestCase.SilvaTestCase):
    def afterSetUp(self):
        self.forum = self.addObject(self.getRoot(), 'Forum', 'forum1',
                                    title='Forum', product='SilvaForum')
        self.thread = self.addObject(self.forum, 'Thread', 'thread1',
                                     title='Thread', product='SilvaForum')
        self.view = getMultiAdapter((self.thread, self.app.REQUEST),
                                    name=u'index.html')

    def test_format_datetime(self):
        # XXX this needs to either be removed, or test something useful...
        dt = DateTime('2007/01/01 01:00')
        self.assertEquals('2007/01/01 01:00:00 GMT+1',
                          self.view.format_datetime(dt))

    def test_unicode_form_save_problems(self):
        self.view.request['title'] = u'F\u00fb'.encode('UTF-8')
        self.view.request['text'] = u'b\u00e4r'.encode('UTF-8')

        self.view.update()

class CommentTest(SilvaTestCase.SilvaTestCase):
    def afterSetUp(self):
        self.forum = self.addObject(self.getRoot(), 'Forum', 'forum1',
                                    title='Forum', product='SilvaForum')
        self.thread = self.addObject(self.forum, 'Thread', 'thread1',
                                     title='Thread', product='SilvaForum')
        self.comment = self.addObject(self.thread, 'Comment', 'comment1',
                                      title='Comment', product='SilvaForum')

    def test_comment(self):
        self.assertEquals('Comment', self.comment.get_title())
        self.assertEquals('', self.comment.get_text())

        self.comment.set_text('foo text')
        self.assertEquals('foo text', self.comment.get_text())

class CommentViewTest(SilvaTestCase.SilvaTestCase):
    def afterSetUp(self):
        self.forum = self.addObject(self.getRoot(), 'Forum', 'forum1',
                                    title='Forum', product='SilvaForum')
        self.thread = self.addObject(self.forum, 'Thread', 'thread1',
                                     title='Thread', product='SilvaForum')
        self.comment = self.addObject(self.thread, 'Comment', 'comment1',
                                      title='Comment', product='SilvaForum')
        self.view = getMultiAdapter((self.comment, self.app.REQUEST),
                                    name=u'index.html')

    def test_format_text(self):
        text = 'foo bar'
        self.assertEquals('foo bar', self.view.format_text(text))
        text = 'foo\nbar'
        self.assertEquals('foo<br />bar', self.view.format_text(text))
        text = 'foo<bar'
        self.assertEquals('foo&lt;bar', self.view.format_text(text))

import unittest
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ForumTest))
    suite.addTest(unittest.makeSuite(ThreadTest))
    suite.addTest(unittest.makeSuite(ThreadViewTest))
    suite.addTest(unittest.makeSuite(CommentTest))
    suite.addTest(unittest.makeSuite(CommentViewTest))
    return suite

