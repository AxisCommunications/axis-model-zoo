#!/bin/sh

echo "Cleaning log"
for file in /var/log/info.*; do
	echo /dev/null >"$file"
done
echo "Log cleaned"

echo "Reading SoC"
SoC=$(parhandclient getgroup root.Properties.System.Soc | cut -d "\"" -f 2)

if [ "$SoC" = "Ambarella CV25" ]; then
	echo "Testing models via cv25"
	folder="./models/cv25/"
	chip="ambarella-cvflow"
elif [ "$SoC" = "Axis Artpec-8" ]; then
	folder="./models/artpec8/"
	chip="axis-a8-dlpu-tflite"
elif [ "$SoC" = "Axis Artpec-7" ]; then
	folder="./models/artpec7/"
	chip="google-edge-tpu-tflite"
else
	echo "No models for this SoC"
	exit 1
fi

echo "Running tests using chip: $chip"
# for all the files in the folder
for file in "$folder"*; do
	echo "Testing $file"
	larod_out=$(larod-client -R 1000 -p -c $chip -g "$file" -i '' | grep "Mean execution time for job:")
	echo "result: $file $larod_out"
done
echo "Done"