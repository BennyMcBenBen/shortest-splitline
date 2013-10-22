'''
census_downloader.py downloads the block files from the census website.

@author Ben Zoller
'''

import csv
import os
import urllib.request
import zipfile

import state_csv_parser
from census import Census
from state import State
from state_districts import StateDistricts

def download(url, download_dir):
  if not os.path.exists(download_dir):
    os.makedirs(download_dir)
  file_name = url.split('/')[-1]
  u = urllib.request.urlopen(url)
  f = open(download_dir + file_name, 'wb')
  file_size = int(u.getheader("Content-Length"))
  print("Downloading: {} Bytes: {}".format(file_name, file_size))
  file_size_dl = 0
  block_sz = 8192
  while True:
    buffer = u.read(block_sz)
    if not buffer:
      break
    file_size_dl += len(buffer)
    f.write(buffer)
    percent = file_size_dl * 100. / file_size
    status = "{:10d}  [{:3.2f}%]".format(file_size_dl, percent)
    status = status + chr(8)*(len(status)+1)
    print(status, end=" ")
  f.close()

def extract_block_file(zip_file, download_dir, state, census):
  block_file_name = get_block_file_name(state, census)
  print("Extracting {}...".format(block_file_name))
  zip_file.extract(block_file_name, download_dir)

def extract_geo_file(zip_file, download_dir, state, census):
  geo_file_name = get_geo_file_name(state, census)
  print("Extracting {}...".format(geo_file_name))
  zip_file.extract(geo_file_name, download_dir)

def get_block_file_name(state, census):
  return census.block_file.format(state.abbrev.lower())

def get_geo_file_name(state, census):
  return census.geo_file.format(state.abbrev.lower())

def get_csv_file_name(state):
  return "{}.csv".format(state.abbrev.lower()) 

def get_zip_file_name(state, census):
  return census.zip_file.format(state.abbrev.lower())

def download_state_zip(download_dir, state, census):
  zip_file_name = get_zip_file_name(state, census)
  url = "{}/{}/{}".format(census.url, state.name, zip_file_name)
  download(url, download_dir)

def extract_state_census_files(download_dir, state, census):
  zip_file_name = get_zip_file_name(state, census)
  try:
    with open(download_dir + zip_file_name): pass
  except IOError as e:
    download_state_zip(download_dir, state, census)
  zip_file = zipfile.ZipFile(download_dir + zip_file_name, "r")
  extract_block_file(zip_file, download_dir, state, census)
  extract_geo_file(zip_file, download_dir, state, census)
  zip_file.close()
  print("Deleting {}...".format(zip_file_name))
  os.remove(download_dir + zip_file_name)

def build_pop_dict(block_file_path):
  pop = {}
  with open(block_file_path, 'r') as block_file:
    block_reader = csv.reader(block_file)
    for block_row in block_reader:
      block_id = block_row[4]
      block_pop = block_row[5]
      pop[block_id] = block_pop
  return pop 

def write_csv(download_dir, state, census):
  try:
    with open(download_dir + get_block_file_name(state, census)): pass
    with open(download_dir + get_geo_file_name(state, census)): pass
  except IOError as e:
    extract_state_census_files(download_dir, state, census)
  block_file_name = get_block_file_name(state, census)
  pop = build_pop_dict(download_dir + block_file_name)
  csv_file_name = get_csv_file_name(state)
  with open(download_dir + csv_file_name, 'w') as csv_file:
    csv_writer = csv.writer(csv_file)
    geo_file_name = get_geo_file_name(state, census)
    with open(download_dir + geo_file_name, 'r') as geo_file:
      for line in geo_file:
        region = line[census.region_start:census.region_end]
        if region == "101":
          block_id = line[census.block_start:census.block_end]
          tract = line[census.tract_start:census.tract_end]
          group = line[census.group_start:census.group_end]
          lat = line[census.lat_start:census.lat_end]
          lon = line[census.lon_start:census.lon_end]
          block_pop = pop[block_id]
          row = [tract, group, block_id, block_pop, lat, lon]
          csv_writer.writerow(row)
  print("Wrote {}".format(csv_file_name))    

def prepare_state(state, census):
  print("Preparing {} {}...".format(state.name, census.year))
  download_dir = "{}/{}/{}/".format(download_dir_root, census.year, 
    state.abbrev)
  try:
    with open(download_dir + get_csv_file_name(state)): pass
  except IOError as e:
    write_csv(download_dir, state, census)

def prepare_states():
  states = state_csv_parser.read_states_csv()
  for state in states.values():
    prepare_state(state)

download_dir_root = "temp"

def build_census_dict():
  census = {}
  census[2000] = Census(2000,
    "http://www2.census.gov/census_2000/datasets/Summary_File_1", 
    "{}00001_uf1.zip", "{}00001.uf1", "{}geo.uf1",
    8, 11, 18, 25, 55, 61, 61, 62, 310, 319, 319, 329)
  census[2010] = Census(2010,
    "http://www2.census.gov/census_2010/04-Summary_File_1", 
    "{}2010.sf1.zip", "{}000012010.sf1", "{}geo2010.sf1",
    8, 11, 18, 25, 54, 60, 60, 61, 336, 347, 347, 359)
  return census

if __name__ == "__main__":
  year = 2010
  states = state_csv_parser.read_states_csv()
  state_districts = state_csv_parser.read_state_districts_csv(states, year)
  census = build_census_dict()[year] 

  al = states['AL']
  ak = states['AK']
  md = states['MD']
  pa = states['PA']

  prepare_state(al, census)
  prepare_state(ak, census)
  prepare_state(md, census)
  prepare_state(pa, census)
