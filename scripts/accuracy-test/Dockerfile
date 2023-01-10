ARG ARCH=armv7hf
ARG VERSION=1.4
ARG UBUNTU_VERSION=22.04
ARG REPO=axisecp
ARG SDK=acap-native-sdk

FROM ${REPO}/${SDK}:${VERSION}-${ARCH}-ubuntu${UBUNTU_VERSION}

# Copy the library to application folder
WORKDIR /opt/app
COPY ./app .

# Download models and labels
RUN mkdir -p model && \
    curl -o model/mobilenet_v2_1.0_224_quant.tgz \
    http://download.tensorflow.org/models/tflite_11_05_08/mobilenet_v2_1.0_224_quant.tgz && \
    tar -xvf model/mobilenet_v2_1.0_224_quant.tgz -C model && \
    rm -f model/*.tgz model/*.pb* model/*.ckpt* model/*.meta model/*.txt && \
    curl -L -o model/mobilenet_v2_1.0_224_quant_edgetpu.tflite \
    https://raw.githubusercontent.com/google-coral/test_data/master/tf2_mobilenet_v2_1.0_224_ptq_edgetpu.tflite && \
    curl -L -o model/mobilenet_v2_cavalry.bin \
    https://acap-ml-model-storage.s3.amazonaws.com/mobilenetv2_cavalry.bin
RUN mkdir -p label && \
    curl -L -o label/imagenet_labels.txt \
    https://github.com/google-coral/edgetpu/raw/master/test_data/imagenet_labels.txt
RUN mkdir -p ground
COPY app/ground_truth.txt ground/

ARG CHIP=
# Building the ACAP application
RUN if [ "$CHIP" = cpu ] || [ "$CHIP" = artpec8 ]; then \
        cp /opt/app/manifest.json.${CHIP} /opt/app/manifest.json && \
        . /opt/axis/acapsdk/environment-setup* && acap-build . \
        -a 'label/imagenet_labels.txt' -a 'model/mobilenet_v2_1.0_224_quant.tflite' -a 'ground/ground_truth.txt'; \
    elif [ "$CHIP" = edgetpu ]; then \
        cp /opt/app/manifest.json.${CHIP} /opt/app/manifest.json && \
        . /opt/axis/acapsdk/environment-setup* && acap-build . \
        -a 'label/imagenet_labels.txt' -a 'model/mobilenet_v2_1.0_224_quant_edgetpu.tflite' -a 'ground/ground_truth.txt'; \
    elif [ "$CHIP" = cv25 ]; then \
        cp /opt/app/manifest.json.${CHIP} /opt/app/manifest.json && \
        . /opt/axis/acapsdk/environment-setup* && acap-build . \
        -a 'label/imagenet_labels.txt' -a 'model/mobilenet_v2_cavalry.bin' -a 'ground/ground_truth.txt'; \
    else \
        printf "Error: '%s' is not a valid value for the CHIP variable\n", "$CHIP"; \
        exit 1; \
    fi
