*Copyright (C) 2023, Axis Communications AB, Lund, Sweden. All Rights Reserved.*

# Axis Model Zoo

Axis network cameras can be used for computer vision applications and can run machine learning models to make inferences. The model to use will depend on your device and your application. This repository contains a collection of different models compatible with Axis cameras and some performance measures (accuracy and speed). Our goal is to keep updating this collection with models for different applications, like object detection or pose estimation. For easy reproduction, we mostly use models that are public and we also share tools to benchmark the models. We have linked the model files and, in case they are public, the ckpt files to continue the training. The values of speed and accuracy are going to be updated with every [AXIS OS release](https://help.axis.com/axis-os-release-notes).

> **Note** : These are not production-quality models, they are off-the-shelf models used for comparative and demonstration purposes only.

## Guides

- [ACAP Documentation](https://axiscommunications.github.io/acap-documentation/)
- [Run YOLOv5 on Artpec-8](./docs/yolov5-on-artpec8.md)

## Models

### Image classification

| Platform | Model | TF version | Speed | Accuracy |
| ---------- | ---------- | :----------: | :----------: | :----------: |

| ARTPEC-7 (Q1615 Mk III) | [MobilenetV2](https://raw.githubusercontent.com/google-coral/test_data/master/mobilenet_v2_1.0_224_quant_edgetpu.tflite) ([ckpt](http://download.tensorflow.org/models/tflite_11_05_08/mobilenet_v2_1.0_224_quant.tgz)) | 1 | <!--A7_tf1_mnv2--> 4.37 ms <!--end_A7_tf1_mnv2--> | Top 1: 68.9% <br/> Top 5: 88.2% |
| ARTPEC-7 (Q1615 Mk III) | [MobilenetV2](https://raw.githubusercontent.com/google-coral/test_data/master/tf2_mobilenet_v2_1.0_224_ptq_edgetpu.tflite) | 2 | <!--A7_tf2_mnv2--> 4.41 ms <!--end_A7_tf2_mnv2--> | Top 1: 69.6% <br/> Top 5: 89.1%  |
| ARTPEC-7 (Q1615 Mk III) | [MobilenetV3](https://raw.githubusercontent.com/google-coral/test_data/master/tf2_mobilenet_v3_edgetpu_1.0_224_ptq_edgetpu.tflite) | 2 | <!--A7_tf2_mnv3--> 4.50 ms <!--end_A7_tf2_mnv3--> | Top 1: 72.7% <br/> Top 5: 91.1% |
| ARTPEC-8 (P1465-LE) | [MobilenetV2](https://raw.githubusercontent.com/google-coral/test_data/master/mobilenet_v2_1.0_224_quant.tflite) ([ckpt](http://download.tensorflow.org/models/tflite_11_05_08/mobilenet_v2_1.0_224_quant.tgz)) | 1  | <!--A8_P_tf1_mnv2--> 9.88 ms <!--end_A8_P_tf1_mnv2--> | Top 1: 68.8% <br/> Top 5: 88.9% |
| ARTPEC-8 (Q1656-LE)  | [MobilenetV2](https://raw.githubusercontent.com/google-coral/test_data/master/mobilenet_v2_1.0_224_quant.tflite) ([ckpt](http://download.tensorflow.org/models/tflite_11_05_08/mobilenet_v2_1.0_224_quant.tgz)) | 1  | <!--A8_tf1_mnv2--> 5.33 ms <!--end_A8_tf1_mnv2--> | Top 1: 68.8% <br/> Top 5: 88.9% |
| CV25 (M3085-V) | [MobilenetV2](https://acap-ml-model-storage.s3.amazonaws.com/mobilenetv2_cavalry.bin) ([ckpt](http://download.tensorflow.org/models/tflite_11_05_08/mobilenet_v2_1.0_224_quant.tgz)) | 1  | <!--cv25_tf1_mnv2--> 28.79 ms <!--end_cv25_tf1_mnv2--> | Top 1: 66.7% <br/> Top 5: 87.1% |
| CV25 (M3085-V) | [EfficientNet-Lite0](https://acap-ml-model-storage.s3.amazonaws.com/EfficientNet-lite0.bin) ([ckpt](https://storage.googleapis.com/cloud-tpu-checkpoints/efficientnet/lite/efficientnet-lite0.tar.gz)) | 1  | <!--cv25_tf1_ens--> 35.31 ms <!--end_cv25_tf1_ens--> | Top 1: 71.2% <br/> Top 5: 90.3% |

### Object detection

| Platform | Model  | Speed | Accuracy |
| ---------- | ---------- |  :----------: | :----------: |
| ARTPEC-7 (Q1615 Mk III) | [SSD MobileNet v2](https://raw.githubusercontent.com/google-coral/test_data/master/ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite)  | <!--A7_tf1_ssd_mnv2--> 17.01 ms <!--end_A7_tf1_ssd_mnv2--> | mAP: 25.6% |
| ARTPEC-7 (Q1615 Mk III) | [SSDLite MobileDet](https://raw.githubusercontent.com/google-coral/test_data/master/ssdlite_mobiledet_coco_qat_postprocess_edgetpu.tflite)  | <!--A7_tf1_ssd_md--> 29.56 ms <!--end_A7_tf1_ssd_md--> | mAP: 32.9% |
| ARTPEC-8 (P1465-LE) | [SSD MobilenetV2](https://raw.githubusercontent.com/google-coral/test_data/master/ssd_mobilenet_v2_coco_quant_postprocess.tflite)  | <!--A8_P_tf1_ssd_mnv2--> 29.34 ms <!--end_A8_P_tf1_ssd_mnv2--> | mAP: 25.6% |
| ARTPEC-8 (P1465-LE) | [SSDLite MobileDet](https://raw.githubusercontent.com/google-coral/test_data/master/ssdlite_mobiledet_coco_qat_postprocess.tflite)  | <!--A8_P_tf1_ssd_md--> 40.99 ms <!--end_A8_P_tf1_ssd_md--> | mAP: 32.9% |
| ARTPEC-8 (P1465-LE)  | [Yolov5n-Artpec8](https://acap-ml-model-storage.s3.amazonaws.com/yolov5/yolov5n.tflite) ([ckpt](https://acap-ml-model-storage.s3.amazonaws.com/yolov5/yolov5n.pt))  | <!--A8_P_yolov5n--> 100.00 ms <!--end_A8_P_yolov5n--> | mAP: 23.5% |
| ARTPEC-8 (Q1656-LE)  | [SSD MobilenetV2](https://raw.githubusercontent.com/google-coral/test_data/master/ssd_mobilenet_v2_coco_quant_postprocess.tflite)  | <!--A8_Q_tf1_ssd_mnv2--> 18.81 ms <!--end_A8_Q_tf1_ssd_mnv2--> | mAP: 25.6% |
| ARTPEC-8 (Q1656-LE)  | [SSDLite MobileDet](https://raw.githubusercontent.com/google-coral/test_data/master/ssdlite_mobiledet_coco_qat_postprocess.tflite)  | <!--A8_Q_tf1_ssd_md--> 30.81 ms <!--end_A8_Q_tf1_ssd_md--> | mAP: 32.9%  |
| ARTPEC-8 (Q1656-LE)  | [Yolov5n-Artpec8](https://acap-ml-model-storage.s3.amazonaws.com/yolov5/yolov5n.tflite) ([ckpt](https://acap-ml-model-storage.s3.amazonaws.com/yolov5/yolov5n.pt))  | <!--A8_Q_yolov5n--> 54.86 ms <!--end_A8_Q_yolov5n--> | mAP: 23.5%  |
| ARTPEC-8 (Q1656-LE)  | [Yolov5s-Artpec8](https://acap-ml-model-storage.s3.amazonaws.com/yolov5/yolov5s.tflite) ([ckpt](https://acap-ml-model-storage.s3.amazonaws.com/yolov5/yolov5s.pt))  | <!--A8_Q_yolov5s--> 69.42 ms <!--end_A8_Q_yolov5s--> | mAP: 32.3%  |
| ARTPEC-8 (Q1656-LE)  | [Yolov5m-Artpec8](https://acap-ml-model-storage.s3.amazonaws.com/yolov5/yolov5m.tflite) ([ckpt](https://acap-ml-model-storage.s3.amazonaws.com/yolov5/yolov5m.pt))  | <!--A8_Q_yolov5m--> 94.81 ms <!--end_A8_Q_yolov5m--> | mAP: 37.9%  |

*Values for AXIS OS 11.9.60.*

## How are the measures calculated?

The [auto-test-framework](./scripts/auto-test-framework) directory holds the code for measuring the speed numbers and automating their update in the repository. For now, the accuracy measures are not included in this pipeline. Apart from that, in the [accuracy-test](./scripts/accuracy-test) there is the code to measure the accuracy and [model_performance_tester.py](./scripts/model_performance_tester.py) is a script to measure the speed.

### Speed measure

In the case of the automated test framework, the test is done by installing and running an ACAP application on the Axis camera. To know more about how it works, see the [larod-test](./scripts/auto-test-framework/larod-test) directory.

To get speed measures more easily, you can use the code in [model_performance_tester.py](./scripts/model_performance_tester.py). This script connects to the Axis camera via SSH and uses the `larod-client` to run inferences. It then parses the output, which will be the mean of time the Axis camera spent on the inferences. These inferences are done on randomly generated images. See below how to use the script:

```sh
python3 ./model_performance_tester.py \
        --model_path <MODEL_PATH> --test_duration <DURATION> \
        --chip <CHIP> --device_ip <IP> --device_credentials <USER> <PASS> --camera_port <SSH_PORT>
```

where, `<MODEL_PATH>` is the path where your `.tflite` or `.bin` model is and `<DURATION>` is the amount of inferences to run. The rest are camera parameters.

### Accuracy measure

This test is done by installing and running an ACAP application on the Axis camera. To know more about how it works, see the [accuracy-test](./scripts/accuracy-test/) directory.

## License

[Apache 2.0](./LICENSE)
