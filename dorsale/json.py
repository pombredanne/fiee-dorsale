# -*- coding: utf-8 -*-
"""
JSON helpers

by Felipe Prenholato, from http://chronosbox.org/blog/jsonresponse-in-django?lang=en
"""
from django.db.models.base import ModelBase
from django.http import HttpResponseForbidden, HttpResponse
from django.utils import simplejson
from django.utils.encoding import force_unicode

class LazyJSONEncoder(simplejson.JSONEncoder):
    """
    A JSONEncoder subclass that handle querysets and models objects.
    
    Add your code about how to handle your type of object here to use
    when dumping JSON."""
    def default(self, o):
        # this handles querysets and other iterable types
        try:
            iterable = iter(o)
        except TypeError:
            pass
        else:
            return list(iterable)
 
        # this handles Models
        try:
            isinstance(o.__class__, ModelBase)
        except Exception:
            pass
        else:
            return force_unicode(o)
 
        return super(LazyJSONEncoder,self).default(obj)
 
def serialize_to_json(obj, *args, **kwargs):
    """
    Wrap simplejson.dumps with defaults as:
 
    :ensure_ascii: False
    :cls: LazyJSONEncoder
 
    All arguments can be added via kwargs.
    """
    kwargs['ensure_ascii'] = kwargs.get('ensure_ascii',False)
    kwargs['cls'] = kwargs.get('cls',LazyJSONEncoder)
 
    return simplejson.dumps(obj,*args,**kwargs)
 
class JSONResponse(HttpResponse):
    """
    JSON response class
    """
    def __init__(self, content='', json_opts={}, mimetype="application/json", *args, **kwargs):
        """
        Return an response object with JSON content 
        using `serialize_to_json`, that is a wrapper to `simplejson.dumps`
        method using a custom class to handle models and querysets.

        Put your options to `serialize_to_json` in `json_opts`, 
        other options are used by response.
        """
        if content:
            content = serialize_to_json(content, **json_opts)
        else:
            content = serialize_to_json([], **json_opts)
        super(JSONResponse,self).__init__(content, mimetype, *args, **kwargs)
