#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from django.utils.translation import ugettext_lazy as _
import os
import re
import hashlib
import unicodedata
#from dorsale.conf import settings

def get_hash_path(instance, source_filename, target_filename=''):
    """
    Create a hashed path for a file - no real security, just hard to guess.
    """
    if hasattr(instance, 'pk'):
        id = str(instance.pk)
    else:
        id = instance.__hash__()
    if not target_filename:
        fn, ext = os.path.splitext(source_filename.lower())
        target_filename = "%s_%s%s" % (instance.__class__.__name__, id, ext)
    path = os.path.join(instance.__class__.__module__.replace('.models', ''), instance.__class__.__name__, hashlib.md5(id).hexdigest(), target_filename)
    return path

def slugify(text):
    """Convert `text` to a harmless, URL-ready, lowercase ASCII string."""
    if type(text) is str:
        text = unicode(text, 'utf-8')
    text = unicodedata.normalize('NFKD', text.lower()).encode('ASCII', 'ignore')
    text = re.sub(r'[^\w\d\-]+', '', text)
    return text.replace(' ', '_').replace('__', '_').replace('--', '-')

def assert_on_exception(fn):
    """
    This decorator cares that exceptions raised by the wrapped widget won’t get swallowed by Django.
    
    In custom Django widgets or admin list_display callable functions you have probably run into this: 
    Everything looks ok, except the place where your widget should be is just blank. 
    Nothing. No traceback or any clue as to what went wrong.

    It seems that Django suppresses all the exceptions sent by widgets rendering 
    except for AssertionError and TypeError. Debugging under those conditions is tricky, 
    so I wrote a function decorator to help. 
    Just import this and put @assert_on_exception before your render method or admin list_display callable function.
    
    by Ian Ward, http://excess.org/article/2010/12/django-hides-widget-exceptions/
    """
    import sys
    def wrap(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except (AssertionError, TypeError):
            raise
        except:
            assert 0, sys.exc_info()[0].__name__ + ": " + str(sys.exc_info()[1])
    wrap.__name__ = fn.__name__
    wrap.__dict__.update(fn.__dict__)
    wrap.__doc__ = fn.__doc__
    wrap.__module__ = fn.__module__
    return wrap