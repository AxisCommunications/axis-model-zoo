# YOLOv5 on Axis cameras

Starting from Axis OS 11.7, ARTPEC-8 supports YOLOv5. It is also supported by ARTPEC-9 cameras. To achieve the best performance, Axis provides a patch that needs to be applied to the YOLOv5 repository before training. We have tested the model sizes yolov5n, yolov5s, and yolov5m, and we recommend sticking with these sizes to avoid exceeding the device memory. Please note that for ARTPEC-8 these models were tested on a Q1656 device with 2GB of RAM. For ARTPEC-9 they were tested on a Q1728 device with 4GB of RAM. Devices with less memory may encounter issues when handling larger models.

## How to Train YOLOv5 for ARTPEC-8

### 1. Clone the YOLOv5 repository and apply the patch

> [!NOTE]
>
> To comply with the [licensing terms of Ultralytics](https://github.com/ultralytics/yolov5?tab=readme-ov-file#license),
> the patch applied here is licensed under AGPL-3.0-only. The license file is available together
> with the patch, see [LICENSE](https://acap-ml-models.s3.amazonaws.com/yolov5/YOLOv5_LICENSE.txt).

```bash
git clone https://github.com/ultralytics/yolov5
cd yolov5
git checkout 95ebf68f92196975e53ebc7e971d0130432ad107
```

Download the model patch and apply it. 
> [!NOTE]
>
> You need to download the correct patch for your device's system-on-chip (ARTPEC-8 or ARTPEC-9).

For **ARTPEC-8**:
```bash
curl -L https://acap-ml-models.s3.amazonaws.com/yolov5/yolov5_artpec8.patch | git apply
```

For **ARTPEC-9**:
```bash
curl -L https://acap-ml-models.s3.amazonaws.com/yolov5/yolov5_artpec9.patch | git apply
```

Install the required libraries located in requirements file in the yolov5 repository.
```bash
pip install -r requirements.txt
```

### 2. Train the model

```bash
python3 train.py --name axis-train --data coco.yaml --epochs 300 --weights '' --cfg yolov5n.yaml  --batch-size 128
```

> [!Note]
>
>Instead of using coco.yaml as the dataset, you can use your own dataset. Visit the [Yolov5 train on custom data](https://docs.ultralytics.com/yolov5/tutorials/train_custom_data/) guide to learn how to annotate your own dataset.

We also provide checkpoint weights for yolov5n, yolov5s, and yolov5m, which you can use as a starting point for your training. To use these weights as a starting point, you can use the --weights flag in the train.py command above.

### 3. Export the model

Export the model for **ARTPEC-8**:
```bash
python3 export.py --weights runs/train/axis-train/weights/best.pt --include tflite --int8 --per-tensor
```

Export the model for **ARTPEC-9**:
```bash
python3 export.py --weights runs/train/axis-train/weights/best.pt --include tflite --int8
```

### 4. (Optional) Evaluate the model accuracy

```bash
python3 val.py --weights runs/train/axis-train/weights/best-int8.tflite
```

In this step, you may want to provide the --data flag and your own dataset to run validation.

### 5. (Optional) Evaluate the model speed

You can use the [model performance tester](https://github.com/AxisCommunications/axis-model-zoo/blob/main/scripts/model_performance_tester.py) script in the [Axis Model Zoo](https://github.com/AxisCommunications/axis-model-zoo/tree/main) to evaluate the model's speed on the target device.

```bash
curl -OL https://raw.githubusercontent.com/AxisCommunications/axis-model-zoo/main/scripts/model_performance_tester.py
pip install paramiko
python3 model_performance_tester.py --model_path runs/train/axis-train/weights/best-int8.tflite --test_duration 100 \\
        --chip <CHIP> --device_ip <IP> --device_credentials <USER> <PASS>
```

For more details on testing the model, refer to the
[Test Your Model](https://axiscommunications.github.io/acap-documentation/docs/computer-vision-on-device/test-your-model.html)
page in the ACAP documentation.

### 6. (Optional) Run example ACAP application with your model

In the [acap-native-sdk-examples](https://github.com/AxisCommunications/acap-native-sdk-examples), there is an example called [object-detection-yolov5](https://github.com/AxisCommunications/acap-native-sdk-examples/tree/main/object-detection-yolov5) that demonstrates how to use a YOLOv5 model in a native ACAP application. By default the application downloads a pre-trained model, but it is possible to edit the example to use your own YOLOv5 model and labels file instead. See the [Dockerfile parameter](https://github.com/AxisCommunications/acap-native-sdk-examples/tree/main/object-detection-yolov5#dockerfile-parameters) section of the [README](https://github.com/AxisCommunications/acap-native-sdk-examples/tree/main/object-detection-yolov5) for specific instructions.

### 7. Checkpoints

Checkpoints and performance measurements for yolov5n, yolov5s, and yolov5m are available in the
readme of [Axis Model Zoo](../README.md).

## License

[Apache 2.0](../LICENSE)
