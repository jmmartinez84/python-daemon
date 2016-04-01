import ConfigParser

class settings(object):
	@staticmethod
	def get(name):
		config = ConfigParser.RawConfigParser()
		config.read('settings.cfg')
		list_items = config.items(name)
		return dict(list_items)