#!/bin/sh

# script to build an OS-X disk image from the wxNUCOS app

rm -rf temp_dist
mkdir temp_dist
# note: the R means it will preserve dynamic links -- critical!
cp -fR dist/NUCOS.app temp_dist/

/usr/bin/hdiutil create -format ULMO -srcfolder temp_dist -volname "NUCOS 4.1.0 Disk Image" -ov "NUCOS-4.1.0"

