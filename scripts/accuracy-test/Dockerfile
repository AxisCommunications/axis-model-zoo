# syntax=docker/dockerfile:1

ARG ARCH=armv7hf
ARG VERSION=12.2.0
ARG UBUNTU_VERSION=24.04
ARG REPO=axisecp
ARG SDK=acap-native-sdk

FROM ${REPO}/${SDK}:${VERSION}-${ARCH}-ubuntu${UBUNTU_VERSION}

# Copy the library to application folder
WORKDIR /opt/app
COPY ./app .

# Download models and labels and copy ground truth
RUN <<EOF
mkdir -p model
curl -o model/mobilenet_v2_1.0_224_quant.tgz \
    http://download.tensorflow.org/models/tflite_11_05_08/mobilenet_v2_1.0_224_quant.tgz
tar -xvf model/mobilenet_v2_1.0_224_quant.tgz -C model
rm -f model/*.tgz model/*.pb* model/*.ckpt* model/*.meta model/*.txt
curl -L -o model/mobilenet_v2_1.0_224_quant_edgetpu.tflite \
    https://raw.githubusercontent.com/google-coral/test_data/master/tf2_mobilenet_v2_1.0_224_ptq_edgetpu.tflite
curl -L -o model/mobilenet_v2_cavalry.bin \
    https://acap-ml-models.s3.amazonaws.com/mobilenet/mobilenet_v2_cv25_imagenet_224.bin
EOF

RUN <<EOF
mkdir -p label
curl -L -o label/imagenet_labels.txt \
    https://github.com/google-coral/edgetpu/raw/master/test_data/imagenet_labels.txt
mkdir -p ground
EOF

COPY app/ground_truth.txt ground/

ARG CHIP=
# Building the ACAP application
RUN <<EOF
if [ "$CHIP" = cpu ] || [ "$CHIP" = artpec8 ] || [ "$CHIP" = artpec9 ]; then
    cp /opt/app/manifest.json.${CHIP} /opt/app/manifest.json
    . /opt/axis/acapsdk/environment-setup*
    acap-build . -a 'label/imagenet_labels.txt' -a 'model/mobilenet_v2_1.0_224_quant.tflite' -a 'ground/ground_truth.txt'
elif [ "$CHIP" = edgetpu ]; then
    cp /opt/app/manifest.json.${CHIP} /opt/app/manifest.json
    . /opt/axis/acapsdk/environment-setup*
    acap-build . -a 'label/imagenet_labels.txt' -a 'model/mobilenet_v2_1.0_224_quant_edgetpu.tflite' -a 'ground/ground_truth.txt'
elif [ "$CHIP" = cv25 ]; then
    cp /opt/app/manifest.json.${CHIP} /opt/app/manifest.json
    . /opt/axis/acapsdk/environment-setup*
    acap-build . -a 'label/imagenet_labels.txt' -a 'model/mobilenet_v2_cavalry.bin' -a 'ground/ground_truth.txt'
else
    printf "Error: '%s' is not a valid value for the CHIP variable\n", "$CHIP"
    exit 1
fi
EOF
