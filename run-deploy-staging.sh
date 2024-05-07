#! /bin/bash

# Copyright (c) 2024 Streetlives, Inc.
# 
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.


echo "make sure you git committed all your other stuff!"
echo "i'm gonna update requirements.txt here and git commit it just fyi"

pip freeze > requirements.txt

# to deploy you need this
sed -i '' -e 's/psycopg2/psycopg2\-binary/' requirements.txt

# remove awsebcli
sed -i '' -e 's/awsebcli.*//' requirements.txt

# remove botocore
sed -i '' -e 's/botocore.*//' requirements.txt

# remove jupyter
sed -i '' -e 's/jupyter.*//g' requirements.txt

# remove djlint
sed -i '' -e 's/djlint.*//g' requirements.txt

# remove black
sed -i '' -e 's/black.*//g' requirements.txt

# remove GDAL
sed -i '' -e 's/GDAL.*//g' requirements.txt

git add requirements.txt

git commit -m "update requirements.txt"

eb deploy yourpeer-test
