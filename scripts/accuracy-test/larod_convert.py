#!/usr/bin/env python3

# Copyright (C) 2023 Axis Communications AB, Lund, Sweden
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0>
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Conversion of image bitmaps to raw bytes.

import argparse
import os
import sys
from math import ceil
import cv2
import numpy as np
class ConvertImage:
    """Convert image to binary image"""
    # pylint: disable=too-many-instance-attributes
    def __init__(self, separate_planes,  # pylint: disable=too-many-arguments
                 height, width, images, output_filename,
                 to_float, px_div, px_sub,
                 alignment, pitch):
        self.separate_planes = separate_planes
        self.height = height
        self.width = width
        self.images = images
        self.output_filename = output_filename
        self.to_float = to_float
        self.px_div = px_div
        self.px_sub = px_sub
        self.alignment = alignment
        self.pitch = pitch
    def write_data(self, binary_file, data, width_bytes, pitch_bytes=0):
        """Write data to disk"""
        if pitch_bytes in (width_bytes, 0):
            # No padding needed, write data as is
            binary_file.write(data.tobytes())
        else:
            self.write_data_with_padding(binary_file,
                                         data,
                                         width_bytes,
                                         pitch_bytes)
    @staticmethod
    def write_data_with_padding(binary_file, data,
                                width_bytes, pitch_bytes):
        """Add padding and write data to binary file"""
        padding_size = pitch_bytes - width_bytes
        i = 0
        for byte in data.tobytes():
            binary_file.write(bytes([byte]))
            i += 1
            if i % width_bytes == 0:
                binary_file.write(b'\0' * padding_size)
    def check_arguments(self):
        """Check option conditions"""
        if not self.to_float and (self.px_div != 1 or self.px_sub != 0):
            sys.exit("ERROR: Options \"--px-division\" and "
                     "\"--px-subtraction\" "
                     "requires option \"--float\"")
        if self.alignment > 0 and self.pitch > 0:
            sys.exit('Not allowed to use both alignment and pitch')
    def convert(self):
        """Convert images"""
        self.check_arguments()
        for img_file in os.listdir(self.images):
            self.output_filename = 'output/' + os.path.splitext(img_file)[0] + '.bin'
            img = cv2.imread(self.images + '/' + img_file)
            if img is None:
                print("WARNING: Could not read image", self.images + '/' + img_file)
                continue
            # size in bytes for one row
            width_bytes = self.width
            # OpenCV reads the image in BGR order.
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            if self.to_float:
                img = cv2.resize(img,
                                 (self.width, self.height)).astype(np.float32)
                img -= self.px_sub
                img /= self.px_div
                # float is used, 4 bytes per pixel
                width_bytes *= 4
            else:
                img = cv2.resize(img, (self.width, self.height))
            if not self.separate_planes:
                # RGB interleaved each pixel is containing r, g and b data
                width_bytes *= 3
            if self.alignment > 0:
                self.pitch = int(ceil(width_bytes / float(self.alignment)) *
                                 self.alignment)
            if self.separate_planes:
                r_val, g_val, b_val = cv2.split(img)
                with open(self.output_filename, 'wb') as output_file:
                    self.write_data(output_file, r_val, width_bytes,
                                    self.pitch)
                    self.write_data(output_file, g_val, width_bytes,
                                    self.pitch)
                    self.write_data(output_file, b_val, width_bytes,
                                    self.pitch)
            else:
                with open(self.output_filename, 'wb') as output_file:
                    self.write_data(output_file, img, width_bytes, self.pitch)
            print("Output file written to {}".format(self.output_filename))
def non_empty_str(string):
    """Verify that string is not empty"""
    if not string:
        raise argparse.ArgumentTypeError("string is empty")
    return string
def positive_int(string):
    """Convert string to int and verify that it is positive"""
    nbr = int(string)
    if nbr <= 0:
        raise argparse.ArgumentTypeError(string + " is not greater than zero")
    return nbr
def non_negative_int(string):
    """Convert string to int and verify that it is not negative"""
    nbr = int(string)
    if nbr < 0:
        raise argparse.ArgumentTypeError(string + " is not non-negative")
    return nbr
def non_negative_float(string):
    """Convert string to float and verify that it is not negative"""
    nbr = float(string)
    if nbr < 0:
        raise argparse.ArgumentTypeError(string + " is not non-negative")
    return nbr
if __name__ == '__main__':
    # Argument parsing.
    PARSER = argparse.ArgumentParser(description="Read and convert bitmap "
                                     "images to raw bytes.")
    PARSER.add_argument("-p", "--separate-planes", action="store_true",
                        default=False, help="Create separated color planes. "
                        "Default is interleaved RGB colors.")
    PARSER.add_argument("height", metavar="HEIGHT", type=positive_int,
                        help="Resize IMAGE's height to HEIGHT.")
    PARSER.add_argument("width", metavar="WIDTH", type=positive_int,
                        help="Resize IMAGE's width to WIDTH.")
    PARSER.add_argument("images", metavar="IMAGE",
                        type=non_empty_str,
                        help="Input image files.")
    PARSER.add_argument("-o", "--output", metavar="FILE", type=non_empty_str,
                        dest="output_filename",
                        help="Output file name for the converted image. "
                        "Default is input image base name with suffix "
                        "\"_RGB_HEIGHTxWIDTH.bin\".")
    PARSER.add_argument("-f", "--float", action="store_true", default=False,
                        dest="to_float",
                        help="Convert pixel values to float (32-bit).")
    PARSER.add_argument("-s", "--px-division", metavar="S",
                        type=non_negative_float, dest="px_div", default=1,
                        help="Divide the pixel values with S when converting "
                        "to float (see option \"--float\"). Default is 1, "
                        "i.e. no division.")
    PARSER.add_argument("-m", "--px-subtraction", metavar="M",
                        type=non_negative_float, dest="px_sub", default=0,
                        help="Subtract the pixel values with M when "
                        "converting to float (see option \"--float\"). "
                        "Default is 0, i.e. no subtraction.")
    PARSER.add_argument("-a", "--alignment", metavar="A",
                        type=non_negative_int, dest="alignment", default=0,
                        help="Row alignment in bytes. Rows will be padded to "
                             "a multiple of the alignment. Not to be used "
                             "when pitch is used")
    PARSER.add_argument("-w", "--pitch", metavar="P",
                        type=non_negative_int, dest="pitch", default=0,
                        help="Row pitch in bytes. Rows will be padded to "
                             "match the pitch. Not to be used when alignment "
                             "is used")
    PARSER.add_argument("-v", "--version", action="version")
    ARGUMENTS = PARSER.parse_args()
    CONVERT_IMAGE = ConvertImage(**vars(ARGUMENTS))
    CONVERT_IMAGE.convert()
