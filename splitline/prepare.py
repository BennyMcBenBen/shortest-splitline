'''
prepare.py provides utilities for downloading and processing state census files.

@author: Ben Zoller
'''
import csv
import os
import urllib2
import zipfile

def download(url, download_dir):
  if not os.path.exists(download_dir):
	    os.makedirs(download_dir)
  file_name = url.split('/')[-1]
  u = urllib2.urlopen(url)
  f = open(download_dir + file_name, 'wb')
  meta = u.info()
  file_size = int(meta.getheaders("Content-Length")[0])
  print "Downloading: %s Bytes: %s" % (file_name, file_size)
  file_size_dl = 0
  block_sz = 8192
  while True:
    buffer = u.read(block_sz)
    if not buffer:
      break
    file_size_dl += len(buffer)
    f.write(buffer)
    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
    status = status + chr(8)*(len(status)+1)
    print status,
  f.close()

def extract_block_file(zip_file, download_dir, state_abbr):
  block_file_name = get_block_file_name(state_abbr)
  print "Extracting %s..." % (block_file_name)
  zip_file.extract(block_file_name, download_dir)

def extract_geo_file(zip_file, download_dir, state_abbr):
  geo_file_name = get_geo_file_name(state_abbr)
  print "Extracting %s..." % (geo_file_name)
  zip_file.extract(geo_file_name, download_dir)

def get_block_file_name(state_abbr):
  return state_abbr + "000012010.sf1"

def get_geo_file_name(state_abbr):
  return state_abbr + "geo2010.sf1"

def get_csv_file_name(state_abbr):
  return state_abbr + '.csv' 

def get_zip_file_name(state_abbr):
  return state_abbr + "2010.sf1.zip"

def download_state_zip(download_dir, state_abbr, state_name):
  zip_file_name = get_zip_file_name(state_abbr)
  url = "http://www2.census.gov/census_2010/04-Summary_File_1/" + state_name + "/" + zip_file_name
  download(url, download_dir)

def extract_state_census_files(download_dir, state_abbr, state_name):
  zip_file_name = state_abbr + "2010.sf1.zip"
  try:
    with open(download_dir + zip_file_name): pass
  except IOError as e:
    download_state_zip(download_dir, state_abbr, state_name)
  zip_file = zipfile.ZipFile(download_dir + zip_file_name, "r")
  extract_block_file(zip_file, download_dir, state_abbr)
  extract_geo_file(zip_file, download_dir, state_abbr)
  zip_file.close()
  print "Deleting %s..." % (zip_file_name)
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

def write_csv(download_dir, state_abbr, state_name):
  try:
    with open(download_dir + get_block_file_name(state_abbr)): pass
    with open(download_dir + get_geo_file_name(state_abbr)): pass
  except IOError as e:
    extract_state_census_files(download_dir, state_abbr, state_name)
  block_file_name = get_block_file_name(state_abbr)
  pop = build_pop_dict(download_dir + block_file_name)
  csv_file_name = get_csv_file_name(state_abbr)
  with open(download_dir + csv_file_name, 'w') as csv_file:
    csv_writer = csv.writer(csv_file)
    geo_file_name = get_geo_file_name(state_abbr)
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
  print "Wrote %s" % (csv_file_name)    

def prepare_state(abbr, name):
  print "Preparing %s..." % (name)
  download_dir = download_dir_root + abbr + "/"
  try:
    with open(download_dir + get_csv_file_name(abbr)): pass
  except IOError as e:
    write_csv(download_dir, abbr, name)

def prepare_states():
  states = init_states()
  for abbr, name in sorted(states.iteritems()):
    prepare_state(abbr, name)

def init_states():
  return {
    'al': 'Alabama',
    'ak': 'Alaska',
    'az': 'Arizona',
    'ar': 'Arkansas',
    'ca': 'California',
    'co': 'Colorado',
    'ct': 'Connecticut',
    'de': 'Delaware',
    'dc': 'District_of_Columbia',
    'fl': 'Florida',
    'ga': 'Georgia',
    'hi': 'Hawaii',
    'id': 'Idaho',
    'il': 'Illinois',
    'in': 'Indiana',
    'ia': 'Iowa',
    'ks': 'Kansas',
    'ky': 'Kentucky',
    'la': 'Louisiana',
    'me': 'Maine',
    'md': 'Maryland',
    'ma': 'Massachusetts',
    'mi': 'Michigan',
    'mn': 'Minnesota',
    'ms': 'Mississippi',
    'mo': 'Missouri',
    'mt': 'Montana',
    'ne': 'Nebraska',
    'nv': 'Nevada',
    'nh': 'New_Hampshire',
    'nj': 'New_Jersey',
    'nm': 'New_Mexico',
    'ny': 'New_York',
    'nc': 'North_Carolina',
    'nd': 'North_Dakota',
    'oh': 'Ohio',
    'ok': 'Oklahoma',
    'or': 'Oregon',
    'pa': 'Pennsylvania',
    'pr': 'Puerto_Rico',
    'ri': 'Rhode_Island',
    'sc': 'South_Carolina',
    'sd': 'South_Dakota',
    'tn': 'Tennessee',
    'tx': 'Texas',
    'ut': 'Utah',
    'vt': 'Vermont',
    'va': 'Virginia',
    'wa': 'Washington',
    'wv': 'West_Virginia',
    'wi': 'Wisconsin',
    'wy': 'Wyoming'
  }

def get_num_districts():
  return {
    'al': 7,
    'ak': 1,
    'az': 9,
    'ar': 4,
    'ca': 53,
    'co': 7,
    'ct': 5,
    'de': 1,
    'dc': 0,
    'fl': 27,
    'ga': 14,
    'hi': 2,
    'id': 2,
    'il': 18,
    'in': 9,
    'ia': 4,
    'ks': 4,
    'ky': 6,
    'la': 6,
    'me': 2,
    'md': 8,
    'ma': 9,
    'mi': 14,
    'mn': 8,
    'ms': 4,
    'mo': 8,
    'mt': 1,
    'ne': 3,
    'nv': 4,
    'nh': 2,
    'nj': 12,
    'nm': 3,
    'ny': 27,
    'nc': 13,
    'nd': 1,
    'oh': 16,
    'ok': 5,
    'or': 5,
    'pa': 18,
    'pr': 0,
    'ri': 2,
    'sc': 7,
    'sd': 1,
    'tn': 9,
    'tx': 36,
    'ut': 4,
    'vt': 1,
    'va': 11,
    'wa': 10,
    'wv': 3,
    'wi': 8,
    'wy': 1
  }

download_dir_root = "../../resources/"

prepare_states()
