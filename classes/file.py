import os.path
import mimetypes
import random
import re

def exists(name):
	return os.path.isfile("files/{}".format(name))

def get_content(name):
	f = open("files/{}".format(name), "rb")
	content = f.read()
	f.close()
	return content

def mime(name):
	return mimetypes.MimeTypes().guess_type("files/{}".format(name))[0]

def get_src(html_content):
	r = re.compile(rb'src="(.+?)"', re.MULTILINE)
	return r.findall(html_content)