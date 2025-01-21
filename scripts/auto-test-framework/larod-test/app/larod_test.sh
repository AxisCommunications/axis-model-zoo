#!/bin/sh

# Copyright (C) 2023 Axis Communications AB, Lund, Sweden
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0>
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

echo "Reading device model"
model=$(parhandclient getgroup root.Brand.ProdNbr | cut -d "\"" -f 2)
echo "Model name:$model."

echo "Reading SoC"
SoC=$(parhandclient getgroup root.Properties.System.Soc | cut -d "\"" -f 2)

if [ "$SoC" = "Ambarella CV25" ]; then
	echo "Testing models via cv25"
	folder="./models/cv25/"
	chip="ambarella-cvflow"
elif [ "$SoC" = "Axis Artpec-9" ]; then
	folder="./models/artpec9/"
	chip="a9-dlpu-tflite"
elif [ "$SoC" = "Axis Artpec-8" ]; then
	folder="./models/artpec8/"
	chip="axis-a8-dlpu-tflite"
elif [ "$SoC" = "Axis Artpec-7" ]; then
	folder="./models/artpec7/"
	chip="google-edge-tpu-tflite"
else
	echo "No models for SoC $SoC"
	exit 1
fi

echo "Running tests using chip: $chip"
# for all the files in the folder
for file in "$folder"*; do
	echo "Testing $file"
	larod_out=$(larod-client -R 1000 -w 5 -p -c $chip -g "$file" -i '' | grep "Mean execution time for job:")
	echo "result: $file $larod_out"
done
echo "Done"
