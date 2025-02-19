*Copyright (C) 2023, Axis Communications AB, Lund, Sweden. All Rights Reserved.*

# Accuracy test ACAP application written in C

This README file briefly explains how this ACAP application works.

## Getting started

Below is the structure and scripts used in the example:

```sh
accuracy-test
├── app
│   ├── accuracy_measure.c
│   ├── argparse.c
│   ├── argparse.h
│   ├── ground_truth.txt
│   ├── LICENSE
│   ├── Makefile
│   └── manifest.json.*
├── Dockerfile
├── larod_convert.py
├── rename_files.py
├── LOC_synset_mapping.txt
└── README.md
```

- **app/accuracy_measure.c** - Accuracy testing code, written in C.
- **app/argparse.c/h** - Implementation of argument parser, written in C.
- **app/ground_truth.txt** - Annotations to the testing dataset.
- **app/LICENSE** - Text file which lists all open source licensed source code distributed with the application.
- **app/Makefile** - Makefile containing the build and link instructions for building the ACAP application.
- **app/manifest.json.\*** - Defines the application and its configuration when building for different chips.
- **Dockerfile** - Docker file with the specified Axis toolchain and API container to build the example specified.
- **larod_convert.py** - Implementation of conversion of images to raw bytes.
- **rename_files.py** - Script that renames the images files.
- **LOC_synset_mapping.txt** - Text file that maps the class codes of the dataset to their friendly names.
- **README.md** - Step by step instructions on how to run the example.

## How to run the code

This application uses `larod` to load a neural network model to make inferences and the results are later processed and compared in [accuracy_measure.c](./app/accuracy_measure.c). The accuracy measure has several steps and it depends on what model are we measuring. Here we are going to explain how we measured the image classification models using the validation dataset of the [ILSVRC2012](https://www.image-net.org/index.php) dataset.

Prerequisites:

- You have enabled [Developer Mode]((https://developer.axis.com/acap/get-started/set-up-developer-environment/set-up-device-advanced/#developer-mode)) on your device.
- You have downloaded the [ILSVRC2012](https://www.image-net.org/index.php) validation dataset containing 50,000 images.

To to run the code, follow these instructions:

1. First, build the Docker image with the following commands:

    ```sh
    DOCKER_BUILDKIT=1 docker build --no-cache --tag <APP_IMAGE> --build-arg CHIP=<CHIP> --build-arg ARCH=<ARCH> .
    docker cp $(docker create <APP_IMAGE>):/opt/app ./build
    ```

    - `<APP_IMAGE>` is the name to tag the image with, e.g., `accuracy-test:1.0`
    - `<CHIP>` is the chip type. Supported values are `artpec8`, `cpu`, `cv25` and `edgetpu`.
    - `<ARCH>` is the architecture. Supported values are `armv7hf` (default) and `aarch64`.

    In this example, model and label files are downloaded from <https://coral.ai/models/>,
    when building the application. Different devices support different chips and models.
    Which model that is used is configured through attributes in `manifest.json` and the
    `<CHIP>` parameter in the Dockerfile. The attributes in `manifest.json.*` are:
    - `runOptions`, which contains the application command line options.
    - `friendlyName`, a user friendly package name which is also part of the .eap file name.

2. Once you have the EAP file, the uploading is done through `upload.cgi`:

    ```sh
    curl -u <USER:PASS> -F"file=@<APP_FILE_PATH>" <DEVICE_IP>/axis-cgi/applications/upload.cgi
    ```

3. To prepare the ILSVRC2012 validation dataset, the image files has to be renamed from e.g., `ILSVRC2012_val_00013453.JPEG` to `13453.JPEG`, in order for the ACAP application to match the images to the ground truth. This Python script will copy the files with the correct name to `./dataset`:

   ```sh
   python3 rename_files.py <VAL_DIR> ./dataset
   ```

    `<VAL_DIR>` should be the path to the ILSVRC2012 validation folder that contains the `ILSVRC2012_val_*.JPEG` images.

4. Larod makes inference on `.bin` files, so it is necessary to convert the images as shown below, where the arguments are image height, image width, and the location of the correctly named images, `./dataset`:

    ```sh
    python3 larod_convert.py 224 224 ./dataset
    ```

5. For access to the device's SD card, you need to have [Developer Mode](https://developer.axis.com/acap/get-started/set-up-developer-environment/set-up-device-advanced/#developer-mode) set up. If you do, an account named `acap-accuracy_measure` will be available in `System`->`Accounts`->`SSH accounts` through the device's web interface. To be able to ssh into the device and add the images, you will need to add a password for that ssh account by clicking `Update SSH account` from the three dots.

6. Create an imagenet directory in the devices's SD card and copy the converted image files to that directory:

    ```sh
    ssh acap-accuracy_measure@<DEVICE_IP> mkdir -p /var/spool/storage/SD_DISK/imagenet
    ```

    ```sh
    scp .ouputs/ acap-accuracy_measure@<DEVICE_IP>:/var/spool/storage/SD_DISK/imagenet/
    ```

7. Start the application. The logs will list which images have been considered as Top-1, Top-5 or neither. At the end, you will see the results printed.

## License

**[Apache License 2.0](./app/LICENSE)**
