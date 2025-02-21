#!/usr/bin/env python3

# Copyright (C) 2025 Axis Communications AB, Lund, Sweden
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

# Script that renames the images files.

import sys, os

images = sys.argv[1]
output = sys.argv[2]

os.system("mkdir " + output)

for file in os.listdir(images):
    os.system("cp " + os.path.join(images, file) + ' ' + os.path.join(output, file.split("_")[-1].lstrip("0")))
