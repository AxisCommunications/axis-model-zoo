# YOLOv5 on ARTPEC-8

Starting from Axis OS 11.7, ARTPEC-8 supports YOLOv5. To achieve the best performance, Axis provides a patch that needs to be applied to the YOLOv5 repository before training. We have tested the model sizes yolov5n, yolov5s, and yolov5m, and we recommend sticking with these sizes to avoid exceeding the device memory. Please note that these models were tested on a Q1656 device with 2GB of RAM. Devices with less memory may encounter issues when handling larger models.

## How to Train YOLOv5 for ARTPEC-8

### 1. Clone the YOLOv5 repository and apply the patch

```bash
git clone https://github.com/ultralytics/yolov5
cd yolov5
git checkout c42aba5b2f0a3e8a0004739ff0d5d0f83f288012
curl -L https://acap-ml-model-storage.s3.amazonaws.com/yolov5/yolov5-axis-A8.patch | git apply
pip install -r requirements.txt
```

### 2. Train the model

```bash
python3 train.py --name axis-train --data coco.yaml --epochs 300 --weights '' --cfg yolov5n.yaml  --batch-size 128
```

**Note:** Instead of using coco.yaml as the dataset, you can use your own dataset. Visit the [Yolov5 train on custom data](https://docs.ultralytics.com/yolov5/tutorials/train_custom_data/) guide to learn how to annotate your own dataset.

We also provide checkpoint weights for yolov5n, yolov5s, and yolov5m, which you can use as a starting point for your training. To use these weights as a starting point, you can use the --weights flag in the train.py command above.

### 3. Export the model

```bash
python3 export.py --weights runs/train/axis-train/weights/best.pt --include tflite --int8 --per-tensor
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
        --chip A8-DLPU --device_ip <IP> --device_credentials <USER> <PASS>
```

### 6. Checkpoints

We provide the following checkpoints for yolov5n, yolov5s, and yolov5m:

|     Name       |  Checkpoint  |   R  | mAP@.5  | mAP@.5:.95 | speed (ms) on Q1656 |
|----------------|--------------|---------|---------|----------|--------------------|
| [yolov5n.tflite](https://acap-ml-model-storage.s3.amazonaws.com/yolov5/yolov5n.tflite) |  [download](https://acap-ml-model-storage.s3.amazonaws.com/yolov5/yolov5n.pt)    |  0.388  |  0.412  |   0.235  |  59.6              |
| [yolov5s.tflite](https://acap-ml-model-storage.s3.amazonaws.com/yolov5/yolov5s.tflite) |  [download](https://acap-ml-model-storage.s3.amazonaws.com/yolov5/yolov5s.pt)    |  0.487  |  0.530  |   0.323  |  74.3              |
| [yolov5m.tflite](https://acap-ml-model-storage.s3.amazonaws.com/yolov5/yolov5m.tflite) |  [download](https://acap-ml-model-storage.s3.amazonaws.com/yolov5/yolov5m.pt)    |  0.547  |  0.592  |   0.379  |  99.8              |

For more details on testing the model, refer to the [Test Your Model](https://axiscommunications.github.io/acap-documentation/docs/computer-vision-on-device/) page in the ACAP documentation.
