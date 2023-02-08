*Copyright (C) 2023, Axis Communications AB, Lund, Sweden. All Rights Reserved.*

# Speed test ACAP application written in shell script

This README file briefly explains how this ACAP application works.

## Getting started

Below is the structure and scripts used in the example:

```sh
larod-test
├── app
│   ├── larod_test.sh
│   ├── Makefile
│   ├── manifest.json
│   └── models
│   │   ├── artpec7
│   │   ├── artpec8
│   │   └── cv25
├── Dockerfile
└── README.md
```

* **app/larod_test.sh** - Shell script application that runs `larod-client` on all the models compatible with the AXIS camera chip.
* **app/Makefile** - Empty Makefile. Necessary for the build process.
* **app/manifest.json** - Defines the application and its configuration.
* **app/models** - Contains all the models that will be tested, organized by architecture.
* **Dockerfile** - Dockerfile with the specified Axis toolchain and API container to build the example.
* **README.md** - Step by step instructions on how to run the example.

## How to run the code

The ACAP application is built in a GitHub action, [benchmark.yml](../../../.github/workflows/benchmark.yml), and installed in different models of cameras (one for each chip). The results are then read by the GitHub action and used to update the main `README.md` of this repository.

In [benchmark.yml](../../../.github/workflows/benchmark.yml), you can see how:

1. First, it builds the Docker image with the following commands:

    ```sh
    DOCKER_BUILDKIT=1 docker build --no-cache --tag <APP_IMAGE> --build-arg CHIP=<CHIP> --build-arg ARCH=<ARCH> .
    docker cp $(docker create <APP_IMAGE>):/opt/app ./build
    ```

    * `<APP_IMAGE>` is the name to tag the image with, e.g., `larod-test:1.0`
    * `<CHIP>` is the chip type. Supported values are `artpec8`, `cpu`, `cv25` and `edgetpu`.
    * `<ARCH>` is the architecture. Supported values are `armv7hf` (default) and `aarch64`.

2. Once you have the EAP file, the uploading is done through `upload.cgi`.
3. `control.cgi` starts the ACAP application.
4. `systemlog.cgi` reads the logs.
5. [readme_update.py](../readme_update.py) reads the logs and updates the main README.md file.

## License

**[Apache License 2.0](./app/LICENSE)**
