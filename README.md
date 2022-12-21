# axis-model-zoo

This repository contains a collection of models compatible and optimized for Axis cameras. For easy reproduction, we mostly use models that are public and we also share tools to benchmark the models. The values of speed and accuracy are going to be updated every Axis OS release.

## Models

### Image classification

| Platform  | Model | TF version | Speed | Accuracy Top-1 | Accuracy Top-5 |
| ------------- | ------------- | ------------- | ------------- | ------------ | ------------ |
| ARTPEC-7 (Q1615 Mk III) | [MobilenetV2](https://raw.githubusercontent.com/google-coral/test_data/master/mobilenet_v2_1.0_224_quant_edgetpu.tflite)  | 1  | <!--A7_tf1_mnv2--> 4.55 ms <!--end_A7_tf1_mnv2--> | 68.9%  | 88.2% |
| ARTPEC-7 (Q1615 Mk III) | [MobilenetV2](https://raw.githubusercontent.com/google-coral/test_data/master/tf2_mobilenet_v2_1.0_224_ptq_edgetpu.tflite)  | 2  | <!--A7_tf2_mnv2--> 4.58 ms <!--end_A7_tf2_mnv2--> | 69.6%  | 89.1%  |
| ARTPEC-7 (Q1615 Mk III) | [MobilenetV3](https://raw.githubusercontent.com/google-coral/test_data/master/tf2_mobilenet_v3_edgetpu_1.0_224_ptq_edgetpu.tflite)  | 2  | <!--A7_tf2_mnv3--> 4.73 ms <!--end_A7_tf2_mnv3--> | 72.7%  | 91.1% |
| ARTPEC-8 (Q1656)  | [MobilenetV2](https://raw.githubusercontent.com/google-coral/test_data/master/mobilenet_v2_1.0_224_quant.tflite)  | 1  | <!--A8_tf1_mnv2--> 7.27 ms <!--end_A8_tf1_mnv2--> | 68.8% | 88.9% |
| ARTPEC-8 (Q1656) | EfficientNetLite0    | 1  | <!--A8_tf1_eff--> ? <!--end_A8_tf1_eff--> | ??  | ?? |
| CV25 (M3085) | [MobilenetV2](https://acap-ml-model-storage.s3.amazonaws.com/mobilenetv2_cavalry.bin)   | 1  | <!--cv25_tf1_mnv2--> 5.55 ms <!--end_cv25_tf1_mnv2--> | 66.7%  | 87.1% |
| CV25 (M3085) | EfficientNetLite0  | 1  | ?  | ??  | ?? |

*Values for Axis OS <!--fw_version--> 11.1 <!--fw_version-->.*
