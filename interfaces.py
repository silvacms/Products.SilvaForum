# Copyright (c) 2007-2012 Infrae. All rights reserved.
# See also LICENSES.txt
# SilvaForum
# Python

from zope.interface import Interface

class IForum(Interface):
    """ Silva Forum is a collection of topics containing comments

        see ITopic and IComment for (respectively) the topic and comment
        interfaces
    """
    def add_topic(topic):
        """ add a topic
        """

    def topics():
        """ return all topics (list)
        """

class ITopic(Interface):
    """ a topic in a forum
    """
    def add_comment(comment):
        """ add a comment
        """

    def comments():
        """ return all comments (list)
        """

    def get_text():
        """ return the text content
        """

    def set_text(text):
        """ set the text content
        """

class IComment(Interface):
    """ a single comment in a forum
    """
    def get_text():
        """ return the text content
        """

    def set_text(text):
        """ set the text content
        """

