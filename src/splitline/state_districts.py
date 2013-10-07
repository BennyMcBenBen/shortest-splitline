class StateDistricts(object):

	def __init__(self, state, districts):
		self.state = state
		self.districts = districts

	def __repr__(self):
		return "StateDistricts=(state={},districts={})".format(self.state, 
			self.districts)
