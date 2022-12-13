*Copyright (C) 2022, Axis Communications AB, Lund, Sweden. All Rights Reserved.*

# larod-test ACAP application written in shell script

This README file briefly explains this ACAP works


## Getting started

These instructions will guide you on how to execute the code. Below is the structure and scripts used in the example:

```bash
larod-test
├── app
│   ├── larod_test
│   ├── LICENSE
│   ├── Makefile
│   ├── manifest.json
│   └── models 
│   │   ├── artpec7
│   │   ├── artpec8
│   │   └── cv25
├── Dockerfile
└── README.md
```

* **app/larod_test** - Shell script application which runs larod client on all the models compatible with the camera architecture.
* **app/LICENSE** - Text file which lists all open source licensed source code distributed with the application.
* **app/Makefile** - Empty Makefile. Necessary for the build process.
* **app/manifest.json** - Defines the application and its configuration.
* **app/models** - Contains all the models that will be tested, divided by architecture.
* **Dockerfile** - Docker file with the specified Axis toolchain and API container to build the example specified.
* **README.md** - Step by step instructions on how to run the example.

### Run the code

The ACAP is built in a [github action](https://github.com/AxisCommunications/axis-model-zoo/blob/main/.github/workflows/speed-test-action.yml) and uploaded to different models of cameras (one for each chip). The results are then read by the github action and used to upload the main readme of this repository.

## License

**[Apache License 2.0](../LICENSE)**
