import exifread
import sys

argv = sys.argv
argc = len(argv)

if argc != 2:
    print("py_exif [filename]")
    exit(-1)

path_name = sys.argv[1]
# Open image file for reading (binary mode)
f = open(path_name, 'rb')

# Return Exif tags
tags = exifread.process_file(f)

for tag in tags.keys():
    if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
        print("%s  =>  %s" % (tag, tags[tag]))