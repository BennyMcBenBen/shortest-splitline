class Census(object):

	def __init__(self, url, region_start, region_end, block_id_start, 
		block_id_end, tract_start, tract_end, group_start, group_end, 
		lat_start, lat_end, lon_start, lon_end):
		self.url = url
		self.region_start = region_start
		self.region_end = region_end
		self.block_id_start = block_id_start
		self.block_id_end = block_id_end
		self.tract_start = tract_start
		self.tract_end = tract_end
		self.group_start = group_start
		self.group_end = group_end
		self.lat_start = lat_start
		self.lat_end = lat_end
		self.lon_start = lon_start
		self.lon_end = lon_end
