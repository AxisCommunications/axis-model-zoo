*Copyright (C) 2023, Axis Communications AB, Lund, Sweden. All Rights Reserved.*

# Axis Model Zoo

Axis network cameras can be used for computer vision applications and can run machine learning models to make inferences. The model to use will depend on your device and your application. This repository contains a collection of different models compatible with Axis cameras and some performance measures (accuracy and speed). Our goal is to keep updating this collection with models for different applications, like object detection or pose estimation. For easy reproduction, we mostly use models that are public and we also share tools to benchmark the models. We have linked the model files and, in case they are public, the ckpt files to continue the training. The speed measurements in the table are updated with every [AXIS OS release](https://help.axis.com/axis-os-release-notes).

> **Note** : These are not production-quality models, they are off-the-shelf models used for comparative and demonstration purposes only.

## Guides

- [ACAP Documentation](https://axiscommunications.github.io/acap-documentation/)
- [Run YOLOv5 on Artpec-8](./docs/yolov5-on-artpec8.md)
- [Run YOLOv5 on Artpec-9](./docs/yolov5-on-artpec9.md)

## Models

### Image classification

| Platform | Model | TF version | Speed | Accuracy |
| ---------- | ---------- | :----------: | :----------: | :----------: |
| ARTPEC-7 (Q1615 Mk III) | [MobilenetV2](https://raw.githubusercontent.com/google-coral/test_data/master/mobilenet_v2_1.0_224_quant_edgetpu.tflite) ([ckpt](http://download.tensorflow.org/models/tflite_11_05_08/mobilenet_v2_1.0_224_quant.tgz)) | 1 | <!--A7_tf1_mnv2--> 4.48 ms <!--end_A7_tf1_mnv2--> | Top 1: 68.9% <br/> Top 5: 88.2% |
| ARTPEC-7 (Q1615 Mk III) | [MobilenetV2](https://raw.githubusercontent.com/google-coral/test_data/master/tf2_mobilenet_v2_1.0_224_ptq_edgetpu.tflite) | 2 | <!--A7_tf2_mnv2--> 4.45 ms <!--end_A7_tf2_mnv2--> | Top 1: 69.6% <br/> Top 5: 89.1%  |
| ARTPEC-7 (Q1615 Mk III) | [MobilenetV3](https://raw.githubusercontent.com/google-coral/test_data/master/tf2_mobilenet_v3_edgetpu_1.0_224_ptq_edgetpu.tflite) | 2 | <!--A7_tf2_mnv3--> 4.61 ms <!--end_A7_tf2_mnv3--> | Top 1: 72.7% <br/> Top 5: 91.1% |
| ARTPEC-8 (P1465-LE) | [MobilenetV2](https://raw.githubusercontent.com/google-coral/test_data/master/mobilenet_v2_1.0_224_quant.tflite) ([ckpt](http://download.tensorflow.org/models/tflite_11_05_08/mobilenet_v2_1.0_224_quant.tgz)) | 1  | <!--A8_P_tf1_mnv2--> 9.81 ms <!--end_A8_P_tf1_mnv2--> | Top 1: 68.8% <br/> Top 5: 88.9% |
| ARTPEC-8 (Q1656-LE)  | [MobilenetV2](https://raw.githubusercontent.com/google-coral/test_data/master/mobilenet_v2_1.0_224_quant.tflite) ([ckpt](http://download.tensorflow.org/models/tflite_11_05_08/mobilenet_v2_1.0_224_quant.tgz)) | 1  | <!--A8_tf1_mnv2--> 5.41 ms <!--end_A8_tf1_mnv2--> | Top 1: 68.8% <br/> Top 5: 88.9% |
| ARTPEC-9 (Q1728)  | [MobilenetV2](https://raw.githubusercontent.com/google-coral/test_data/master/mobilenet_v2_1.0_224_quant.tflite) ([ckpt](http://download.tensorflow.org/models/tflite_11_05_08/mobilenet_v2_1.0_224_quant.tgz)) | 1  | <!--A9_tf1_mnv2--> 2.80 ms <!--end_A9_tf1_mnv2--> | Top 1: 69.1% <br/> Top 5: 89.0% |
| CV25 (M3085-V) | [MobilenetV2](https://acap-ml-models.s3.amazonaws.com/mobilenet/mobilenet_v2_cv25_imagenet_224.bin) ([ckpt](http://download.tensorflow.org/models/tflite_11_05_08/mobilenet_v2_1.0_224_quant.tgz)) | 1  | <!--cv25_tf1_mnv2--> 5.38 ms <!--end_cv25_tf1_mnv2--> | Top 1: 66.8% <br/> Top 5: 87.2% |
| CV25 (M3085-V) | [EfficientNet-Lite0](https://acap-ml-models.s3.amazonaws.com/efficientnet/efficientnet-lite0_cv25_imagenet_300.bin) ([ckpt](https://storage.googleapis.com/cloud-tpu-checkpoints/efficientnet/lite/efficientnet-lite0.tar.gz)) | 1  | <!--cv25_tf1_ens--> 6.89 ms <!--end_cv25_tf1_ens--> | Top 1: 71.2% <br/> Top 5: 90.3% |

### Object detection

| Platform | Model  | Speed | Accuracy |
| ---------- | ---------- |  :----------: | :----------: |
| ARTPEC-7 (Q1615 Mk III) | [SSD MobileNet v2](https://raw.githubusercontent.com/google-coral/test_data/master/ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite)  | <!--A7_tf1_ssd_mnv2--> 17.36 ms <!--end_A7_tf1_ssd_mnv2--> | mAP: 25.6% |
| ARTPEC-7 (Q1615 Mk III) | [SSDLite MobileDet](https://raw.githubusercontent.com/google-coral/test_data/master/ssdlite_mobiledet_coco_qat_postprocess_edgetpu.tflite)  | <!--A7_tf1_ssd_md--> 30.68 ms <!--end_A7_tf1_ssd_md--> | mAP: 32.9% |
| ARTPEC-8 (P1465-LE) | [SSD MobilenetV2](https://raw.githubusercontent.com/google-coral/test_data/master/ssd_mobilenet_v2_coco_quant_postprocess.tflite)  | <!--A8_P_tf1_ssd_mnv2--> 28.74 ms <!--end_A8_P_tf1_ssd_mnv2--> | mAP: 25.6% |
| ARTPEC-8 (P1465-LE) | [SSDLite MobileDet](https://raw.githubusercontent.com/google-coral/test_data/master/ssdlite_mobiledet_coco_qat_postprocess.tflite)  | <!--A8_P_tf1_ssd_md--> 38.44 ms <!--end_A8_P_tf1_ssd_md--> | mAP: 32.9% |
| ARTPEC-8 (P1465-LE)  | [Yolov5n-Artpec8](https://acap-ml-models.s3.amazonaws.com/yolov5/yolov5n_artpec8_coco_640.tflite) ([ckpt](https://acap-ml-models.s3.amazonaws.com/yolov5/yolov5n_artpec8_coco_640.pt))  | <!--A8_P_yolov5n--> 100.00 ms <!--end_A8_P_yolov5n--> | mAP: 23.5% |
| ARTPEC-8 (Q1656-LE)  | [SSD MobilenetV2](https://raw.githubusercontent.com/google-coral/test_data/master/ssd_mobilenet_v2_coco_quant_postprocess.tflite)  | <!--A8_Q_tf1_ssd_mnv2--> 18.55 ms <!--end_A8_Q_tf1_ssd_mnv2--> | mAP: 25.6% |
| ARTPEC-8 (Q1656-LE)  | [SSDLite MobileDet](https://raw.githubusercontent.com/google-coral/test_data/master/ssdlite_mobiledet_coco_qat_postprocess.tflite)  | <!--A8_Q_tf1_ssd_md--> 28.89 ms <!--end_A8_Q_tf1_ssd_md--> | mAP: 32.9%  |
| ARTPEC-8 (Q1656-LE)  | [Yolov5n-Artpec8](https://acap-ml-models.s3.amazonaws.com/yolov5/yolov5n_artpec8_coco_640.tflite) ([ckpt](https://acap-ml-models.s3.amazonaws.com/yolov5/yolov5n_artpec8_coco_640.pt))  | <!--A8_Q_yolov5n--> 55.55 ms <!--end_A8_Q_yolov5n--> | mAP: 23.5%  |
| ARTPEC-8 (Q1656-LE)  | [Yolov5s-Artpec8](https://acap-ml-models.s3.amazonaws.com/yolov5/yolov5s_artpec8_coco_640.tflite) ([ckpt](https://acap-ml-models.s3.amazonaws.com/yolov5/yolov5s_artpec8_coco_640.pt))  | <!--A8_Q_yolov5s--> 70.15 ms <!--end_A8_Q_yolov5s--> | mAP: 32.3%  |
| ARTPEC-8 (Q1656-LE)  | [Yolov5m-Artpec8](https://acap-ml-models.s3.amazonaws.com/yolov5/yolov5m_artpec8_coco_640.tflite) ([ckpt](https://acap-ml-models.s3.amazonaws.com/yolov5/yolov5m_artpec8_coco_640.pt))  | <!--A8_Q_yolov5m--> 95.47 ms <!--end_A8_Q_yolov5m--> | mAP: 37.9%  |
| ARTPEC-9 (Q1728)  | [SSD MobilenetV2](https://raw.githubusercontent.com/google-coral/test_data/master/ssd_mobilenet_v2_coco_quant_postprocess.tflite)  | <!--A9_tf1_ssd_mnv2--> 14.44 ms <!--end_A9_tf1_ssd_mnv2--> | mAP: 25.6% |
| ARTPEC-9 (Q1728)  | [SSDLite MobileDet](https://raw.githubusercontent.com/google-coral/test_data/master/ssdlite_mobiledet_coco_qat_postprocess.tflite)  | <!--A9_tf1_ssd_md--> 25.62 ms <!--end_A9_tf1_ssd_md--> | mAP: 32.9%  |
| ARTPEC-9 (Q1728)  | [Yolov5n-Artpec9](https://acap-ml-models.s3.amazonaws.com/yolov5/yolov5n_artpec9_coco_640.tflite) ([ckpt](https://acap-ml-models.s3.amazonaws.com/yolov5/yolov5n_artpec9_coco_640.pt))  | <!--A9_yolov5n--> 55.02 ms <!--end_A9_yolov5n--> | mAP: 23.3%  |
| ARTPEC-9 (Q1728)  | [Yolov5s-Artpec9](https://acap-ml-models.s3.amazonaws.com/yolov5/yolov5s_artpec9_coco_640.tflite) ([ckpt](https://acap-ml-models.s3.amazonaws.com/yolov5/yolov5s_artpec9_coco_640.pt))  | <!--A9_yolov5s--> 58.83 ms <!--end_A9_yolov5s--> | mAP: 32.2%  |
| ARTPEC-9 (Q1728)  | [Yolov5m-Artpec9](https://acap-ml-models.s3.amazonaws.com/yolov5/yolov5m_artpec9_coco_640.tflite) ([ckpt](https://acap-ml-models.s3.amazonaws.com/yolov5/yolov5m_artpec9_coco_640.pt))  | <!--A9_yolov5m--> 68.64 ms <!--end_A9_yolov5m--> | mAP: 38.1%  |

*Values for AXIS OS 12.5.56.*

> [!NOTE]
>
> - To comply with the
>   [licensing terms of Ultralytics](https://github.com/ultralytics/yolov5?tab=readme-ov-file#license),
>   the YOLOv5 model files in the table above are licensed under AGPL-3.0-only. The license file is
>   available together with the models
>   [here](https://acap-ml-models.s3.amazonaws.com/yolov5/YOLOv5_LICENSE.txt).
> - If you're having trouble downloading a file, right-click the download link and choose “Copy link
>   address”, then paste it into a new tab and press Enter.

## How are the measures calculated?

There are many factors to consider when determining the performance of a machine learning model.
This repository aims to showcase two key performance indicators: inference speed and accuracy. In
the following sections we will describe how they are measured.

### Speed measure

The [auto-test-framework](./scripts/auto-test-framework) directory contains the code for measuring
the average inference (speed) and updating the speed value of each model in the table above. This
test is run for every [AXIS OS release](https://help.axis.com/axis-os-release-notes). The test is
done by installing and running an ACAP application on the Axis camera. To know more about how it
works, see the [larod-test](./scripts/auto-test-framework/larod-test) directory.

If you want to measure the speed of your own models more conveniently, you can use the code in
[model_performance_tester.py](./scripts/model_performance_tester.py). This script connects to the
Axis camera via SSH and uses the command `larod-client` to run a specified number of inferences on
random data. When all inferences has been run, the output from `larod-client` will be parsed to find
the mean inference time. See below how to use the script:

```sh
python3 ./scripts/model_performance_tester.py \
        --model_path <MODEL_PATH> --test_duration <DURATION> \
        --chip <CHIP> --device_ip <IP> --device_credentials <USER> <PASS> --device_port <SSH_PORT>
```

- `<MODEL_PATH>` is the path to your `.tflite` or `.bin` model.
- `<DURATION>` is the number of inferences to run.
- `<CHIP>` is the larod device to use; `CPU`, `A9-DLPU`, `A8-DLPU`, `A7-GPU`, `A7-TPU`, `CV25`.
- `<IP>` is the IP of the device.
- `<USER>`, `<PASS>` are the device credentials.
- `<SSH_PORT>` is the device port for ssh, default is port `22`.

Go to the
[Test your model](https://developer.axis.com/computer-vision/computer-vision-on-device/test-your-model/)
page to learn more about testing machine learning models on Axis devices.

### Accuracy measure

There are no automated tests for the accuracy results and they are not reevaluated for each release
of AXIS OS. However, the image classification models are tested on an Axis camera by installing and
running an ACAP application on the Axis camera. To know more about how it works, see the
[accuracy-test](./scripts/accuracy-test/) directory.

Accuracy test for the object detection models have never been evaluated on an Axis camera. Instead,
the accuracy results come from
[Coral object detection models](https://coral.ai/models/object-detection/), except our
custom-trained YOLOv5, which were evaluated during the "Evaluate the model accuracy" step in the
[YOLOv5 on ARTPEC-8 guide](docs/yolov5-on-artpec8.md) and
[YOLOv5 or ARTPEC-9 guide](docs/yolov5-on-artpec9.md).

## License

[Apache 2.0](./LICENSE)
