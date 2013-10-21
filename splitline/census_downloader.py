'''
census_downloader.py downloads the block files from the census website.

@author Ben Zoller
'''

import csv
import os
import urllib.request
import zipfile

import state_csv_parser
from state import State
from state_districts import StateDistricts

def download(url, download_dir):
  if not os.path.exists(download_dir):
    os.makedirs(download_dir)
  file_name = url.split('/')[-1]
  u = urllib.request.urlopen(url)
  f = open(download_dir + file_name, 'wb')
  meta = u.info()
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
    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / 
      file_size)
    status = status + chr(8)*(len(status)+1)
    print(status, end=" ")
  f.close()

def extract_block_file(zip_file, download_dir, state_abbr):
  block_file_name = get_block_file_name(state_abbr)
  print("Extracting {}...".format(block_file_name))
  zip_file.extract(block_file_name, download_dir)

def extract_geo_file(zip_file, download_dir, state_abbr):
  geo_file_name = get_geo_file_name(state_abbr)
  print("Extracting {}...".format(geo_file_name))
  zip_file.extract(geo_file_name, download_dir)

def get_block_file_name(state_abbr):
  return state_abbr.lower() + "000012010.sf1"

def get_geo_file_name(state_abbr):
  return state_abbr.lower() + "geo2010.sf1"

def get_csv_file_name(state_abbr):
  return state_abbr.lower() + '.csv' 

def get_zip_file_name(state_abbr):
  return state_abbr.lower() + "2010.sf1.zip"

def download_state_zip(download_dir, state):
  zip_file_name = get_zip_file_name(state.abbrev)
  url = "http://www2.census.gov/census_2010/04-Summary_File_1/" + state.name + "/" + zip_file_name
  download(url, download_dir)

def extract_state_census_files(download_dir, state):
  zip_file_name = state.abbrev.lower() + "2010.sf1.zip"
  try:
    with open(download_dir + zip_file_name): pass
  except IOError as e:
    download_state_zip(download_dir, state)
  zip_file = zipfile.ZipFile(download_dir + zip_file_name, "r")
  extract_block_file(zip_file, download_dir, state.abbrev)
  extract_geo_file(zip_file, download_dir, state.abbrev)
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

def write_csv(download_dir, state):
  try:
    with open(download_dir + get_block_file_name(state.abbrev)): pass
    with open(download_dir + get_geo_file_name(state.abbrev)): pass
  except IOError as e:
    extract_state_census_files(download_dir, state)
  block_file_name = get_block_file_name(state.abbrev)
  pop = build_pop_dict(download_dir + block_file_name)
  csv_file_name = get_csv_file_name(state.abbrev)
  with open(download_dir + csv_file_name, 'w') as csv_file:
    csv_writer = csv.writer(csv_file)
    geo_file_name = get_geo_file_name(state.abbrev)
    with open(download_dir + geo_file_name, 'r') as geo_file:
      for line in geo_file:
        region = line[8:11]
        if region == "101":
          block_id = line[18:25]
          tract = line[55:61]
          group = line[61:62]
          lat = line[336:347]
          lon = line[347:359]
          block_pop = pop[block_id]
          row = [tract, group, block_id, block_pop, lat, lon]
          csv_writer.writerow(row)
  print("Wrote {}".format(csv_file_name))    

def prepare_state(state):
  print("Preparing {}...".format(state))
  download_dir = download_dir_root + state.abbrev + "/"
  try:
    with open(download_dir + get_csv_file_name(state.abbrev)): pass
  except IOError as e:
    write_csv(download_dir, state)

def prepare_states():
  states = state_csv_parser.read_states_csv()
  for state in states.values():
    prepare_state(state)

download_dir_root = "temp/"

if __name__ == "__main__":
  states = state_csv_parser.read_states_csv()
  state_districts = state_csv_parser.read_state_districts_csv(states, 2010)

  al = states['AL']
  md = states['MD']

  prepare_state(al)
  prepare_state(md)
  # TODO abstract away the year
  # TODO download the files under directory temp/YEAR/STATE/.
