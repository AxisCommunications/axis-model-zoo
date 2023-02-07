*Copyright (C) 2023, Axis Communications AB, Lund, Sweden. All Rights Reserved.*

# Axis Model Zoo

Axis network cameras can be used for computer vision applications and can run machine learning models to make inferences. The model to use will depend on your device and your application. This repository contains a collection of different models compatible with Axis cameras and some performance measures (accuracy and speed). Our goal is to keep updating this collection with models for different applications, like object detection or pose estimation. For easy reproduction, we mostly use models that are public and we also share tools to benchmark the models. The values of speed and accuracy are going to be updated with every [AXIS OS release](https://help.axis.com/axis-os-release-notes).

> **Note** : These are not production-quality models, they are off-the-shelf models used for comparative and demonstration purposes only.

## Models

### Image classification

| Platform | Model | TF version | Speed | Accuracy Top-1 | Accuracy Top-5 |
| ---------- | ---------- | :----------: | :----------: | :----------: | :----------: |
| ARTPEC-7 (Q1615 Mk III) | [MobilenetV2](https://raw.githubusercontent.com/google-coral/test_data/master/mobilenet_v2_1.0_224_quant_edgetpu.tflite) | 1 | <!--A7_tf1_mnv2--> 4.55 ms <!--end_A7_tf1_mnv2--> | 68.9% | 88.2% |
| ARTPEC-7 (Q1615 Mk III) | [MobilenetV2](https://raw.githubusercontent.com/google-coral/test_data/master/tf2_mobilenet_v2_1.0_224_ptq_edgetpu.tflite)  | 2 | <!--A7_tf2_mnv2--> 4.58 ms <!--end_A7_tf2_mnv2--> | 69.6%  | 89.1%  |
| ARTPEC-7 (Q1615 Mk III) | [MobilenetV3](https://raw.githubusercontent.com/google-coral/test_data/master/tf2_mobilenet_v3_edgetpu_1.0_224_ptq_edgetpu.tflite) | 2 | <!--A7_tf2_mnv3--> 4.74 ms <!--end_A7_tf2_mnv3--> | 72.7% | 91.1% |
| ARTPEC-8 (Q1656)  | [MobilenetV2](https://raw.githubusercontent.com/google-coral/test_data/master/mobilenet_v2_1.0_224_quant.tflite)  | 1  | <!--A8_tf1_mnv2--> 7.26 ms <!--end_A8_tf1_mnv2--> | 68.8% | 88.9% |
| ARTPEC-8 (P3245-LV) | [MobilenetV2](https://raw.githubusercontent.com/google-coral/test_data/master/mobilenet_v2_1.0_224_quant.tflite)  | 1  | <!--A8_P_tf1_mnv2--> 9.48 ms <!--end_A8_P_tf1_mnv2--> | 68.8% | 88.9% |
| CV25 (M3085) | [MobilenetV2](https://acap-ml-model-storage.s3.amazonaws.com/mobilenetv2_cavalry.bin)   | 1  | <!--cv25_tf1_mnv2--> 5.59 ms <!--end_cv25_tf1_mnv2--> | 66.7%  | 87.1% |
| CV25 (M3085) | [EfficientNet-Lite0](https://acap-ml-model-storage.s3.amazonaws.com/EfficientNet-lite0.bin)  | 1  | <!--cv25_tf1_ens--> 7.03 ms <!--end_cv25_tf1_ens--> | 71.2%  | 90.3% |

*Values for AXIS OS 11.1.*

## How are the measures calculated?

The [auto-test-framework](./scripts/auto-test-framework) directory holds the code for measuring the speed numbers and automating their update in the repository. For now, the accuracy measures are not included in this pipeline. Apart from that, in the [accuracy-test](./scripts/accuracy-test) there is the code to measure the accuracy and [model_performance_tester.py](./scripts/model_performance_tester.py) is a script to measure the speed.

### Speed measure

In the case of the automated test framework, the test is done by installing and running an ACAP application on the AXIS camera. To know more about how it works, see the [larod-test](./scripts/auto-test-framework/larod-test) directory.

To get speed measures more easily, you can use the code in [model_performance_tester.py](./scripts/model_performance_tester.py). This script connects to the AXIS camera via SSH and uses the `larod-client` to run inferences. It then parses the output, which will be the mean of time the AXIS camera spent on the inferences. These inferences are done on randomly generated images. See below how to use the script:

```sh
python3 ./model_performance_tester.py \
        --model_path <MODEL_PATH> --test_duration <DURATION> \
        --chip <CHIP> --device_ip <IP> --device_credentials <USER> <PASS> --camera_port <SSH_PORT>
```

where, `<MODEL_PATH>` is the path where your `.tflite` or `.bin` model is and `<DURATION>` is the amount of inferences to run. The rest are camera parameters.

### Accuracy measure

This test is done by installing and running an ACAP application on the AXIS camera. To know more about how it works, see the [accuracy-test](./scripts/accuracy-test/) directory.

## License

[Apache 2.0](./LICENSE)
