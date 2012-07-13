#!/usr/bin/python
#
# A Python wrapper around the Teleportd API.

__author__ = 'Antoine Llorca <antoine@teleportd.com>'
__version__ = '0.1.0'

import datetime
import httplib
import os
import sys
import time
import urllib
import urllib2
import urlparse
import re

try:
	# Python >= 2.6
	import json as simplejson
except ImportError:
	try:
		# Python < 2.6
		import simplejson
	except ImportError:
		try:
			# Google App Engine
			from django.utils import simplejson
		except ImportError:
			raise ImportError, 'Unable to load a JSON library'

class TeleportdError(Exception):
	'''Class handling Teleportd errors'''
	def __init__(self, msg):
		self.msg = msg
	
	def __str__(self):
		return repr(self.msg)

class Teleportd():
	'''Class wrapping the Teleportd API'''
	def __init__(self, key, url='http://api.teleportd.com', port='80'):
		self.key = key
		self.url = url
		self.port = port
	
	def search(self, args):
		'''Performs a search.
		
		Args:
			args:
				An array of search arguments
		
		Returns:
			The search results as a JSON object if
			everything went ok, an error message otherwise
		'''
		search = self.__request('search', args)
		return search['hits'] if search['ok'] else search['error']
		
	def get(self, sha):
		'''Gets a picture.
		
		Args:
			sha:
				The SHA identifier of the picture
		
		Returns:
			The picture as a JSON object if
			everything went ok, an error message otherwise
		'''
		get = self.__request('get', sha)
		return get['hits'] if get['ok'] else get['error']
	
	def __request(self, endpoint, args):
		'''Executes a GET request to the servers with
		   the provided endpoint and args
		
		Args:
			endpoint:
				The API endpoint (e.g. 'search', 'get'...)
			args:
				An array of search arguments
		
		Returns:
			The search results if everything went ok,
			an error message otherwise
		'''
		path = '/%s?user_key=%s&%s' % (endpoint, self.key, urllib.urlencode(args))
		data = simplejson.loads(urllib2.urlopen(self.url + path).read())
		return data
		