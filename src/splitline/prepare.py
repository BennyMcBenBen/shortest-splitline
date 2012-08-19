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

def unzip(download_dir, file_name):
	zip_file = zipfile.ZipFile(download_dir + file_name, "r")
	print "Unzipping: %s ..." % (file_name)
	zip_file.extractall(download_dir)
	zip_file.close()

def prepare_alabama():

	file_name = "al2010.sf1.zip"
	download_dir = "../../resources/al/"
	filepath = download_dir + file_name
	url = "http://www2.census.gov/census_2010/04-Summary_File_1/Alabama/" + file_name

	try:
		with open(filepath) as f: pass
	except IOError as e:
		download(url, download_dir)

	unzip(download_dir, file_name)


prepare_alabama()
