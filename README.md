# osm
## Map Area
Singapore

I have selected Singapore as it is the place I live and work. Also I am working
on my PhD Thesis that requires me to pull some data from OSM so
it is useful to work on Singapore data. The file I downloaded is 379.8 MB.

## Setup

Since the osm file exceeds the limit of Github I placed zipped version of the file. It should be unzipped first. For the database part mongoDB database should be setup on the OS first. 

## Procedure

First I do the counting of the tags according to the first exercise in the
nanodegree, using mapparser.py.

It gives me this;
{'bounds': 1,
 'member': 130673,
 'nd': 2087568,
 'node': 1667063,
 'osm': 1,
 'relation': 2974,
 'tag': 870923,
 'way': 264907}

 The bounds for this file is; bounds minlat="0.807" minlon="103.062" maxlat="1.823" maxlon="104.545"
 which is larger than Singapore so I need to get rid of places that is not in Singapore first.
 But I leave that to next stage after I pass the data to database.

 2nd step in working in the data is to check the tags in the file. My analysis using
 tags.py gave me this result.
 {'lower': 681314, 'lower_colon': 176410, 'other': 13196, 'problemchars': 3}

 3rd step is to check the number of users that worked in this part of the OSM map. And running
 users.py gives me all the unique users that worked in this file, which is 2270.

 In the auditing phase, 2 things I have noted first one is since I have data not only from Singapore
 but also Johor Bahru, which is the neighbouring city, in Malaysia, I need to check if the way is
 in Singapore or in Malaysia.

 And secondly the main assumption used in the class that In English street names end with street type
 does not apply here since there are 4 official languages in Singapore and for example a street name
 can be Jalan Bukit Kakut, Jalan in this case is street for malay and it is in the beginning of the
 street name not in the end. For more information check here; https://en.m.wikipedia.org/wiki/Road_names_in_Singapore


 So I needed to do the audit twice first for english by checking the ends of the words. I used audit_street.py for this purpose. The results are in the streets.txt. And I did the same for malay words which are in the beginning with audit_street_malay.py.

 Lastly by using data.py, I converted the osm XML file into json file which will be used in the mongodb database.



 ## Data Overview

 More info about this is on the pdf.
