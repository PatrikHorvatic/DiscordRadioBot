from __future__ import print_function
import re
import struct
import sys

try:
    import urllib2
except ImportError:  # Python 3
    import urllib.request as urllib2

class Pjesma:

    def __init__(self, link):
        self.url = link #radio stream
        self.encoding = 'latin1' # default: iso-8859-1 for mp3 and utf-8 for ogg streams

    def dohvatiPjesmu(self):
        try:
            request = urllib2.Request(self.url, headers={'Icy-MetaData': 1})  # request metadata
            response = urllib2.urlopen(request)
            print(response.headers, file=sys.stderr)
            metaint = int(response.headers['icy-metaint'])
            for _ in range(10): # # title may be empty initially, try several times
                response.read(metaint)  # skip to metadata
                metadata_length = struct.unpack('B', response.read(1))[0] * 16  # length byte
                metadata = response.read(metadata_length).rstrip(b'\0')
                print(metadata, file=sys.stderr)
                # extract title from the metadata
                m = re.search(br"StreamTitle='([^']*)';", metadata)
                if m:
                    title = m.group(1)
                    if title:
                        break
            else: 
                sys.exit('no title found')
            return title.decode(self.encoding, errors='replace')

        except:
            pass
