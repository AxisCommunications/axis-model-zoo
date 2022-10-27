# axis-model-zoo

This repository contains a collection of models compatible and optimized for axis cameras.
We also provide tools to benchmark the models.

# Models

## Image classification


| Platform  | Model | TF-version | Speed | Accuracy Top-1 | Accuracy Top-5 |
| ------------- | ------------- | ------------- | ------------- | ------------ | ------------ |
| ARTPEC-7 (Q1615 Mk III) | [MobilenetV2](https://raw.githubusercontent.com/google-coral/test_data/master/mobilenet_v2_1.0_224_quant_edgetpu.tflite)  | 1  | 4.55 ms  | 73.2%  | 90.0%  |
| ARTPEC-7 (Q1615 Mk III) | [MobilenetV1](https://raw.githubusercontent.com/google-coral/test_data/master/tf2_mobilenet_v1_1.0_224_ptq_edgetpu.tflite)  | 2  | 4.29 ms  | 69.5%  | 89.8% |
| ARTPEC-7 (Q1615 Mk III) | [MobilenetV2](https://raw.githubusercontent.com/google-coral/test_data/master/tf2_mobilenet_v2_1.0_224_ptq_edgetpu.tflite)  | 2  | 4.58 ms  | 73.2%  | 91.8%  |
| ARTPEC-7 (Q1615 Mk III) | [MobilenetV3](https://raw.githubusercontent.com/google-coral/test_data/master/tf2_mobilenet_v3_edgetpu_1.0_224_ptq_edgetpu.tflite)  | 2  | 4.76 ms  | 77.5%  | 93.6% |
| ARTPEC-8 (Q1656)  | [MobilenetV2](https://raw.githubusercontent.com/google-coral/test_data/master/mobilenet_v2_1.0_224_quant.tflite)  | 1  | 7.38 ms  | 73.2% | 90.0% |
| ARTPEC-8 (Q1656) | EfficientNetLite0    | 1  | ?  | ??  | ??  |
| CV25 (M3085) | [MobilenetV2](https://acap-ml-model-storage.s3.amazonaws.com/mobilenetv2_cavalry.bin)   | 1  | 5.76 ms  | ??  | ??  |
| CV25  | EfficientNetLite0  | 1  | ?  | ??  | ??  |

