#!/usr/bin/python

import sys
import urllib2
import os.path
from xml.etree import ElementTree as etree
# ElementTree Documentation: https://docs.python.org/2/library/xml.etree.elementtree.html

# coniguration file path
config_file = "podcasts.txt"

# get the url from the parameter
# podcast_url = 'http://techdistortion.com/podcasts/pragmatic/feed'

# stores all the podcast feeds
podcast_urls = []

# check if the podcast_url exists
if len(sys.argv) > 1:
    podcast_urls.append(str(sys.argv[1]))
else:
    print "No feed url specified, looking for config file."
    if not os.path.isfile(config_file): 
        print "No podcast feed specified, no config file found. :-("
        sys.exit()
        
    # there should be a file, open it
    with open(config_file) as file:
        podcast_urls = file.readlines()
        
# save to total download size
total_download_size = 0

# go through all the urls and download episodes if neccessary
for podcast_url in podcast_urls:
    # podcast parse
    podcast_file = urllib2.urlopen(podcast_url)
    # read to string
    podcast_data = podcast_file.read()
    # close file because we dont need it anymore
    podcast_file.close()

    # entire feed
    podcast_root = etree.fromstring(podcast_data)
    items = podcast_root.findall('channel/item')

    for entry in items:
        # within each item, find the enclosure tag
        enclosures = entry.findall('enclosure')
        # there should only be one enclosure in there
        enclosure = enclosures[0]
        # in the enclosure tag, find the url attribute
        url = enclosure.attrib['url']
        # get date and the title from the entry itself
        date = entry.findtext('pubDate')
        title = entry.findtext('title')
    
        print title
        print date
    
        # create the file name string
        file_name = url.split('/')[-1]
    
        # check if we already have a file with that name and continue if so
        if os.path.isfile(file_name): 
            print "Episode already downloaded: " + file_name
            continue
    
        # download the file
        episode_file = urllib2.urlopen(url)
        local_file = open(file_name, 'wb')
        meta = episode_file.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        total_download_size += file_size
    
        print "Downloading: %s Bytes: %s" % (file_name, file_size)

        # update the terminal output
        file_size_downloaded = 0
        block_size = 8192
        while True:
            buffer = episode_file.read(block_size)
            if not buffer:
                break

            file_size_downloaded += len(buffer)
            local_file.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_downloaded, file_size_downloaded * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            print status,
        
        print "Done downloading episode."

        local_file.close()

print "All done, total size in Bytes: %10d" % (total_download_size)