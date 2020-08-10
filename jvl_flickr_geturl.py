# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
## run
## > python flickr_GetUrl.py tag number_of_images_to_attempt_to_download
from flickrapi import FlickrAPI
import pandas as pd
#import xml
import xml.etree.ElementTree as ET
from datetime import datetime

key='98424a03eedc5e2c1b5a9b05050f8aff'
secret='2d857e7b8b30ffd1'

tag = 'LARio_Trail'
text = 'Los_Angeles'

MAX_COUNT = 500

flickr = FlickrAPI(key, secret)
photos = flickr.walk(tags=tag,
                        tag_mode='all',
                        extras='geo,tags,views,date_taken,owner_name,url_o,date_upload,description',
                        per_page=50,
                        sort='relevance', 
                        content_type='1'
                        )
                     
count=0
info=[]


db_columns = ["url", "latitude", "longitude", "tags", "date taken", "owner name", "views", "date uploaded", "description"]

rows = []
for photo in photos:

    if count< MAX_COUNT:
        
        print("Fetching info for image number {}".format(count))
        url = photo.get('url_o')
        geo_lat = photo.get('latitude')
        geo_long = photo.get('longitude')
        tags = photo.get('tags').split(" ")
        date_taken = photo.get('datetaken')
        owner_name = photo.get('ownername')
        views = photo.get('views')
        date_upload = int(photo.get('dateupload'))
        date_upload = datetime.utcfromtimestamp(date_upload).strftime('%Y-%m-%d %H:%M:%S')
        photo_desc = photo.get('description')
        
        
        if url is not None:
            count=count+1
            rows.append(
                    {db_columns[0] : url,
                     db_columns[1] : geo_lat,
                     db_columns[2] : geo_long,
                     db_columns[3] : tags,
                     db_columns[4] : date_taken,
                     db_columns[5] : owner_name,
                     db_columns[6] : views,
                     db_columns[7] : date_upload,
                     db_columns[8] : photo_desc
                     }
                    )
            
            photo_response = flickr.photos.getInfo(photo_id=photo.get('id'))
            #photo_xml = photo_response()[0]
            #for f in photo_xml.getiterator():
             #   print(f)
              #  print(f.items())
            
            
    else:
        print("Done fetching info, fetched {} photos out of {}".format(len(info),MAX_COUNT))
        break
db = pd.DataFrame(rows, columns=db_columns)
db.to_csv("LARioTrail.csv")
#info=pd.Series(info)  #saves just fine when single column of data, tried create dataframe and ID column names but traceback
#print("Writing out the urls in the current directory")
#info.to_csv(tag+"_photoinfo.csv")
#print("Done!!!")




