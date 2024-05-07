#!/bin/bash

# Installation of GDAL and dependencies.
# Based on https://gist.github.com/hervenivon/fe3a327bc28b142e51beb38ef11844c0

# Update with your versions.
GEOS_VERSION=3.11.2
GDAL_VERSION=3.6.4
PROJ4_VERSION=9.2.1

sudo yum-config-manager --enable epel
sudo yum -y install make automake gcc gcc-c++ libcurl-devel proj-devel geos-devel

# Compilation work for geos.
mkdir -p "/tmp/geos-${GEOS_VERSION}-build"
cd "/tmp/geos-${GEOS_VERSION}-build"
curl -o "geos-${GEOS_VERSION}.tar.bz2" \
    "http://download.osgeo.org/geos/geos-${GEOS_VERSION}.tar.bz2" \
    && bunzip2 "geos-${GEOS_VERSION}.tar.bz2" \
    && tar xvf "geos-${GEOS_VERSION}.tar"
cd "/tmp/geos-${GEOS_VERSION}-build/geos-${GEOS_VERSION}"
./configure --prefix=/usr/local/geos

# Make in parallel with 2x the number of processors.
make -j $(( 2 * $(cat /proc/cpuinfo | egrep ^processor | wc -l) )) \
 && sudo make install \
 && sudo ldconfig


# Compilation work for proj4.
mkdir -p "/tmp/proj-${PROJ4_VERSION}-build"
cd "/tmp/proj-${PROJ4_VERSION}-build"
curl -o "proj-${PROJ4_VERSION}.tar.gz" \
    "http://download.osgeo.org/proj/proj-${PROJ4_VERSION}.tar.gz" \
    && tar xfz "proj-${PROJ4_VERSION}.tar.gz"
cd "/tmp/proj-${PROJ4_VERSION}-build/proj-${PROJ4_VERSION}"
./configure --prefix=/usr/local/proj4

# Make in parallel with 2x the number of processors.
make -j $(( 2 * $(cat /proc/cpuinfo | egrep ^processor | wc -l) )) \
 && sudo make install \
 && sudo ldconfig


# Compilation work for GDAL
mkdir -p "/tmp/gdal-${GDAL_VERSION}-build"
cd "/tmp/gdal-${GDAL_VERSION}-build"
curl -o "gdal-${GDAL_VERSION}.tar.gz" \
    "http://download.osgeo.org/gdal/${GDAL_VERSION}/gdal-${GDAL_VERSION}.tar.gz" \
    && tar xfz "gdal-${GDAL_VERSION}.tar.gz"
cd "/tmp/gdal-${GDAL_VERSION}-build/gdal-${GDAL_VERSION}"
./configure --prefix=/usr/local/gdal \
            --with-static-proj4=/usr/local/proj4 \
            --without-python

# Make in parallel with 2x the number of processors.
make -j $(( 2 * $(cat /proc/cpuinfo | egrep ^processor | wc -l) )) \
 && sudo make install \
 && sudo ldconfig


# Bundle resources.
cd /usr/local/geos
tar zcvf "/tmp/geos-${GEOS_VERSION}.tar.gz" *

cd /usr/local/proj4
tar zcvf "/tmp/proj4-${PROJ4_VERSION}.tar.gz" *

cd /usr/local/gdal
tar zcvf "/tmp/gdal-${GDAL_VERSION}.tar.gz" *
