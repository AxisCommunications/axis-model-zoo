# axis-model-zoo

This repository contains a collection of models compatible and optimized for axis cameras.
We also provide tools to benchmark the models.

# Models

## Image classification


| Platform  | Model | TF-ver | Speed | Accuracy Top-1 | Accuracy Top-5 |
| ------------- | ------------- | ------------- | ------------- | ------------ | ------------ |
| ARTPEC-7 (Q1615 Mk III) | [MobilenetV2](https://raw.githubusercontent.com/google-coral/test_data/master/mobilenet_v2_1.0_224_quant_edgetpu.tflite)  | 1  | <!--A7_tf1_mnv2--> 4.55 ms <!--end_A7_tf1_mnv2--> | 73.2%  | 90.0%  |
| ARTPEC-7 (Q1615 Mk III) | [MobilenetV1](https://raw.githubusercontent.com/google-coral/test_data/master/tf2_mobilenet_v1_1.0_224_ptq_edgetpu.tflite)  | 2  | <!--A7_tf2_mnv1--> 4.29 ms <!--end_A7_tf2_mnv1--> | 69.5%  | 89.8% |
| ARTPEC-7 (Q1615 Mk III) | [MobilenetV2](https://raw.githubusercontent.com/google-coral/test_data/master/tf2_mobilenet_v2_1.0_224_ptq_edgetpu.tflite)  | 2  | <!--A7_tf2_mnv2--> 4.58 ms <!--end_A7_tf2_mnv2--> | 73.2%  | 91.8%  |
| ARTPEC-7 (Q1615 Mk III) | [MobilenetV3](https://raw.githubusercontent.com/google-coral/test_data/master/tf2_mobilenet_v3_edgetpu_1.0_224_ptq_edgetpu.tflite)  | 2  | <!--A7_tf2_mnv3--> 234234 <!--end_A7_tf2_mnv3--> | 77.5%  | 93.6% |
| ARTPEC-8 (Q1656)  | [MobilenetV2](https://raw.githubusercontent.com/google-coral/test_data/master/mobilenet_v2_1.0_224_quant.tflite)  | 1  | <!--A8_tf1_mnv2--> 234234s <!--end_A8_tf1_mnv2--> | 73.2% | 90.0% |
| ARTPEC-8 (Q1656) | EfficientNetLite0    | 1  | <!--A8_tf1_eff--> ? <!--end_A8_tf1_eff--> | ??  | ??  |
| CV25 (M3085) | [MobilenetV2](https://acap-ml-model-storage.s3.amazonaws.com/mobilenetv2_cavalry.bin)   | 1  | <!--cv25_tf1_mnv2--> 5.57 ms <!--end_cv25_tf1_mnv2--> | ??  | ??  |
| CV25 (M3085) | EfficientNetLite0  | 1  | ?  | ??  | ??  |
