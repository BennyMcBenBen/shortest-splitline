class Census(object):

	def __init__(self, year, url, zip_file, block_file, geo_file,
		region_start, region_end, block_start, block_end, 
		tract_start, tract_end, group_start, group_end, 
		lat_start, lat_end, lon_start, lon_end):
		self.year = year
		self.url = url
		self.zip_file = zip_file
		self.block_file = block_file
		self.geo_file = geo_file 
		self.region_start = region_start # GEOCOMP
		self.region_end = region_end
		self.block_start = block_start # LOGRECNO
		self.block_end = block_end
		self.tract_start = tract_start # TRACT
		self.tract_end = tract_end
		self.group_start = group_start # BLKGRP
		self.group_end = group_end
		self.lat_start = lat_start # INTPTLAT
		self.lat_end = lat_end
		self.lon_start = lon_start # INTPTLON
		self.lon_end = lon_end
