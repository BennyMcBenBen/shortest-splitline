class State(object):

    def __init__(self, name, abbrev):
        self.name = name
        self.abbrev = abbrev

    def __repr__(self):
    	return "State(abbrev={},name={})".format(self.abbrev, self.name)
