# syntax=docker/dockerfile:1

ARG ARCH=armv7hf
ARG VERSION=12.0.0
ARG UBUNTU_VERSION=24.04
ARG REPO=axisecp
ARG SDK=acap-native-sdk

FROM ${REPO}/${SDK}:${VERSION}-${ARCH}-ubuntu${UBUNTU_VERSION}
ARG device

# Building the ACAP application
COPY ./app /opt/app/
WORKDIR /opt/app
RUN <<EOF
mv larod_test.sh larod_test
. /opt/axis/acapsdk/environment-setup*
acap-build . -a "models/${device}/"
EOF
