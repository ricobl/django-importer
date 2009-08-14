# -*- coding: utf-8 -*-

import StringIO
import gzip
import urllib2

def download_file(url, dest):
    """
    Downloads a HTTP resource from `url` and save to `dest`.
    
    Capable of dealing with Gzip compressed content.
    """
    
    # Create the HTTP request
    request = urllib2.Request(url)
    
    # Add the header to accept gzip encoding
    request.add_header('Accept-encoding', 'gzip')
    
    # Open the request
    opener = urllib2.build_opener()
    response = opener.open(request)
    
    # Retrieve data
    data = response.read()
    
    # If the data is compressed, put the data in a stream and decompress
    if response.headers.get('content-encoding', '') == 'gzip':
        stream = StringIO.StringIO(data)
        gzipper = gzip.GzipFile(fileobj=stream)
        data = gzipper.read()
    
    # Write to a file
    f = open(dest, 'wb')
    f.write(data)
    f.close()
