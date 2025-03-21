/**
 * Copyright (C) 2023 Axis Communications AB, Lund, Sweden
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     <http://www.apache.org/licenses/LICENSE-2.0>
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 * This file parses the arguments to the application.
 */

#include "argparse.h"

#include <argp.h>
#include <stdlib.h>

#define KEY_USAGE (127)

static int parsePosInt(char* arg, unsigned long long* i,
                       unsigned long long limit);
static int parseOpt(int key, char* arg, struct argp_state* state);

const struct argp_option opts[] = {
    {"device", 'c', "DEVICE", 0,
     "Chooses device DEVICE to run on, where DEVICE is the enum type larodChip "
     "from the library. If not specified, the default device for a new "
     "connection will be used.",
     0},
    {"labels", 'l', "LABELS", 0,
     "Path to a file labelling classifications. Each row of this file should "
     "consist of a label, and this label will be mapped to the classification "
     "index corresponding to its row number. At most 60 characters from each "
     "row/label will be read.",
     0},
    {"annotations", 'g', "ANNOTATIONS", 0,
     "Path to a file defining the class of each image. Each row of this file should "
     "consist of a number that corresponds to the class number in the labels file"
     "for the specific image.",
     0},
    {"help", 'h', NULL, 0, "Print this help text and exit.", 0},
    {"usage", KEY_USAGE, NULL, 0, "Print short usage message and exit.", 0},
    {0}};
const struct argp argp = {
    opts,
    parseOpt,
    "MODEL WIDTH HEIGHT OUTPUT_SIZE",
    "This is an example app which loads an image classification MODEL to "
    "larod and then uses vdo to fetch frames of size WIDTH x HEIGHT in a yuv "
    "format which are converted to an interleaved rgb format and then sent to "
    "larod for inference on MODEL. OUTPUT_SIZE denotes the size in bytes of "
    "the tensor output by MODEL.\n\nExample call:\n"
    "accuracy-test-app /tmp/mobilenet_v2_1.0_224_quant.tflite 224 224 "
    "1001 -c cpu-tflite "
    "-l /usr/local/packages/accuracy_measure/label/imagenet_labels.txt "
    "-g /usr/local/packages/accuracy_measure/label/ground_truth.txt ",
    NULL,
    NULL,
    NULL};

bool parseArgs(int argc, char** argv, args_t* args) {
    if (argp_parse(&argp, argc, argv, ARGP_NO_HELP, NULL, args)) {
        return false;
    }
    return true;
}

int parseOpt(int key, char* arg, struct argp_state* state) {
    args_t* args = state->input;

    switch (key) {
    case 'c': {
        args->deviceName = arg;
        break;
    }
    case 'l': {
        args->labelsFile = arg;
        break;
    }
    case 'g': {
        args->annotationsFile = arg;
        break;
    }
    case 'h':
        argp_state_help(state, stdout, ARGP_HELP_STD_HELP);
        break;
    case KEY_USAGE:
        argp_state_help(state, stdout, ARGP_HELP_USAGE | ARGP_HELP_EXIT_OK);
        break;
    case ARGP_KEY_ARG:
        if (state->arg_num == 0) {
            args->modelFile = arg;
        } else if (state->arg_num == 1) {
            unsigned long long width;
            int ret = parsePosInt(arg, &width, UINT_MAX);
            if (ret) {
                argp_failure(state, EXIT_FAILURE, ret, "invalid width");
            }
            args->width = (unsigned int) width;
        } else if (state->arg_num == 2) {
            unsigned long long height;
            int ret = parsePosInt(arg, &height, UINT_MAX);
            if (ret) {
                argp_failure(state, EXIT_FAILURE, ret, "invalid height");
            }
            args->height = (unsigned int) height;
        } else if (state->arg_num == 3) {
            unsigned long long outputBytes;
            int ret = parsePosInt(arg, &outputBytes, SIZE_MAX);
            if (ret) {
                argp_failure(state, EXIT_FAILURE, ret, "invalid output size");
            }
            args->outputBytes = (size_t) outputBytes;
        } else {
            argp_error(state, "Too many arguments given");
        }
        break;
    case ARGP_KEY_INIT:
        args->width = 0;
        args->height = 0;
        args->outputBytes = 0;
        args->deviceName = NULL;
        args->modelFile = NULL;
        args->labelsFile = NULL;
        args->annotationsFile = NULL;
        break;
    case ARGP_KEY_END:
        if (state->arg_num != 4) {
            argp_error(state, "Invalid number of arguments given");
        }
        break;
    default:
        return ARGP_ERR_UNKNOWN;
    }

    return 0;
}

/**
 * brief Parses a string as an unsigned long long
 *
 * param arg String to parse.
 * param i Pointer to the number being the result of parsing.
 * param limit Max limit for data type integer will be saved to.
 * return Positive errno style return code (zero means success).
 */
static int parsePosInt(char* arg, unsigned long long* i,
                       unsigned long long limit) {
    char* endPtr;

    *i = strtoull(arg, &endPtr, 0);
    if (*endPtr != '\0') {
        return EINVAL;
    } else if (arg[0] == '-' || *i == 0) {
        return EINVAL;
        // Make sure we don't overflow when casting.
    } else if (*i == ULLONG_MAX || *i > limit) {
        return ERANGE;
    }

    return 0;
}
