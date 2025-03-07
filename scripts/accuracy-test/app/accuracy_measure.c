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
* The application expects four arguments on the command line in the following
 * order: MODEL WIDTH HEIGHT OUTPUT_SIZE.
 *
 * First argument, MODEL, is a string describing path to the model.
 *
 * Second argument, WIDTH, is an integer for width size.
 *
 * Third argument, HEIGHT, is an integer for height size.
 *
 * Fourth argument, OUTPUT_SIZE, denotes the size in bytes of
 * the tensor output by model.
 *
 * The application has four optional arguments on the command line in the following
 * order: DEVICE LABEL GROUND_TRUTH.
 *
 * First optional argument, DEVICE, is a string of the selected larod device.
 *
 * Second optional argument, LABEL, is the path to a file labelling classifications.
 *
 * Finally, fourth optional argument, GROUND_TRUTH, is the path to a file giving
 * the annotations of the images.
 *
 * Then you could run the application with Google TPU with command:
 *     ./usr/local/packages/accuracy_measure/accuracy_measure \
 *     /usr/local/packages/accuracy_measure/model/mobilenet_v2_1.0_224_quant_edgetpu.tflite \
 *     224 224 1001 -c google-edge-tpu-tflite \
 *     -l /usr/local/packages/accuracy_measure/label/imagenet_labels.txt \
 *     -g /usr/local/packages/accuracy_measure/ground/ground_truth.txt"
 */

#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/time.h>
#include <sys/types.h>
#include <syslog.h>
#include <unistd.h>
#include <math.h>
#include <string.h>

#include "argparse.h"
#include "larod.h"

#define N_IMAGES 50000

/**
 * brief Creates a temporary fd truncated to correct size and mapped.
 *
 * This convenience function creates temp files to be used for input and output.
 *
 * param fileName Pattern for how the temp file will be named in file system.
 * param fileSize How much space needed to be allocated (truncated) in fd.
 * param mappedAddr Pointer to the address of the fd mapped for this process.
 * param Pointer to the generated fd.
 * return False if any errors occur, otherwise true.
 */
static bool createAndMapTmpFile(char* fileName, size_t fileSize,
                                void** mappedAddr, int* convFd);

/**
 * brief Sets up and configures a connection to larod, and loads a model.
 *
 * Opens a connection to larod, which is tied to larodConn. After opening a
 * larod connection the devivce specified by deviceName is set for the
 * connection. Then the model file specified by larodModelFd is loaded to the
 * device, and a corresponding larodModel object is tied to model.
 *
 * param deviceName Specifier for which larod device to use.
 * param larodModelFd Fd for a model file to load.
 * param larodConn Pointer to a larod connection to be opened.
 * param model Pointer to a larodModel to be obtained.
 * return False if error has occurred, otherwise true.
 */
static bool setupLarod(const char* deviceName, const int larodModelFd,
                       larodConnection** larodConn, larodModel** model);

/**
 * brief Free up resources held by an array of labels.
 *
 * param labels An array of label string pointers.
 * param labelFileBuffer Heap buffer containing the actual string data.
 */
static void freeLabels(char** labelsArray, char* labelFileBuffer);

/**
 * brief Reads a file of labels into an array.
 *
 * An array filled by this function should be freed using freeLabels.
 *
 * param labelsPtr Pointer to a string array.
 * param labelFileBuffer Pointer to the labels file contents.
 * param labelsPath String containing the path to the labels file to be read.
 * param numLabelsPtr Pointer to number which will store number of labels read.
 * return False if any errors occur, otherwise true.
 */
static bool parseLabels(char*** labelsPtr, char** labelFileBuffer,
                        char* labelsPath, size_t* numLabelsPtr);


static bool createAndMapTmpFile(char* fileName, size_t fileSize,
                                void** mappedAddr, int* convFd) {
    syslog(LOG_INFO, "%s: Setting up a temp fd with pattern %s and size %zu", __func__,
           fileName, fileSize);

    int fd = mkstemp(fileName);
    if (fd < 0) {
        syslog(LOG_ERR, "%s: Unable to open temp file %s: %s", __func__, fileName,
               strerror(errno));
        goto error;
    }

    // Allocate enough space in for the fd.
    if (ftruncate(fd, (off_t) fileSize) < 0) {
        syslog(LOG_ERR, "%s: Unable to truncate temp file %s: %s", __func__, fileName,
               strerror(errno));
        goto error;
    }

    // Remove since we don't actually care about writing to the file system.
    if (unlink(fileName)) {
        syslog(LOG_ERR, "%s: Unable to unlink from temp file %s: %s", __func__,
               fileName, strerror(errno));
        goto error;
    }

    // Get an address to fd's memory for this process's memory space.
    void* data =
        mmap(NULL, fileSize, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);

    if (data == MAP_FAILED) {
        syslog(LOG_ERR, "%s: Unable to mmap temp file %s: %s", __func__, fileName,
               strerror(errno));
        goto error;
    }

    *mappedAddr = data;
    *convFd = fd;

    return true;

error:
    if (fd >= 0) {
        close(fd);
    }

    return false;
}

static bool setupLarod(const char* deviceName, const int larodModelFd,
                       larodConnection** larodConn, larodModel** model) {
    larodError* error = NULL;
    larodConnection* conn = NULL;
    larodModel* loadedModel = NULL;
    bool ret = false;

    // Set up larod connection.
    if (!larodConnect(&conn, &error)) {
        syslog(LOG_ERR, "%s: Could not connect to larod: %s", __func__, error->msg);
        goto end;
    }

    const larodDevice* dev = larodGetDevice(conn, deviceName, 0, &error);

    loadedModel = larodLoadModel(conn, larodModelFd, dev, LAROD_ACCESS_PRIVATE,
                                 "Accuracy test model", NULL, &error);
    if (!loadedModel) {
        syslog(LOG_ERR, "%s: Unable to load model: %s", __func__, error->msg);
        goto error;
    }

    *larodConn = conn;
    *model = loadedModel;

    ret = true;

    goto end;

error:
    if (conn) {
        larodDisconnect(&conn, NULL);
    }

end:
    if (error) {
        larodClearError(&error);
    }

    return ret;
}

void freeLabels(char** labelsArray, char* labelFileBuffer) {
    free(labelsArray);
    free(labelFileBuffer);
}

bool parseLabels(char*** labelsPtr, char** labelFileBuffer, char* labelsPath,
                 size_t* numLabelsPtr) {
    // We cut off every row at 60 characters.
    const size_t LINE_MAX_LEN = 60;
    bool ret = false;
    char* labelsData = NULL;  // Buffer containing the label file contents.
    char** labelArray = NULL; // Pointers to each line in the labels text.

    struct stat fileStats = {0};
    if (stat(labelsPath, &fileStats) < 0) {
        syslog(LOG_ERR, "%s: Unable to get stats for label file %s: %s", __func__,
               labelsPath, strerror(errno));
        return false;
    }

    // Sanity checking on the file size - we use size_t to keep track of file
    // size and to iterate over the contents. off_t is signed and 32-bit or
    // 64-bit depending on architecture. We just check toward 10 MByte as we
    // will not encounter larger label files and both off_t and size_t should be
    // able to represent 10 megabytes on both 32-bit and 64-bit systems.
    if (fileStats.st_size > (10 * 1024 * 1024)) {
        syslog(LOG_ERR, "%s: failed sanity check on labels file size", __func__);
        return false;
    }

    int labelsFd = open(labelsPath, O_RDONLY);
    if (labelsFd < 0) {
        syslog(LOG_ERR, "%s: Could not open labels file %s: %s", __func__, labelsPath,
               strerror(errno));
        return false;
    }

    size_t labelsFileSize = (size_t) fileStats.st_size;
    // Allocate room for a terminating NULL char after the last line.
    labelsData = malloc(labelsFileSize + 1);
    if (labelsData == NULL) {
        syslog(LOG_ERR, "%s: Failed allocating labels text buffer: %s", __func__,
               strerror(errno));
        goto end;
    }

    ssize_t numBytesRead = -1;
    size_t totalBytesRead = 0;
    char* fileReadPtr = labelsData;
    while (totalBytesRead < labelsFileSize) {
        numBytesRead =
            read(labelsFd, fileReadPtr, labelsFileSize - totalBytesRead);

        if (numBytesRead < 1) {
            syslog(LOG_ERR, "%s: Failed reading from labels file: %s", __func__,
                   strerror(errno));
            goto end;
        }
        totalBytesRead += (size_t) numBytesRead;
        fileReadPtr += numBytesRead;
    }

    // Now count number of lines in the file - check all bytes except the last
    // one in the file.
    size_t numLines = 0;
    for (size_t i = 0; i < (labelsFileSize - 1); i++) {
        if (labelsData[i] == '\n') {
            numLines++;
        }
    }

    // We assume that there is always a line at the end of the file, possibly
    // terminated by newline char. Either way add this line as well to the
    // counter.
    numLines++;

    labelArray = malloc(numLines * sizeof(char*));
    if (!labelArray) {
        syslog(LOG_ERR, "%s: Unable to allocate labels array: %s", __func__,
               strerror(errno));
        ret = false;
        goto end;
    }

    size_t labelIdx = 0;
    labelArray[labelIdx] = labelsData;
    labelIdx++;
    for (size_t i = 0; i < labelsFileSize; i++) {
        if (labelsData[i] == '\n') {
            // Register the string start in the list of labels.
            labelArray[labelIdx] = labelsData + i + 1;
            labelIdx++;
            // Replace the newline char with string-ending NULL char.
            labelsData[i] = '\0';
        }
    }

    // If the very last byte in the labels file was a new-line we just
    // replace that with a NULL-char. Refer previous for loop skipping looking
    // for new-line at the end of file.
    if (labelsData[labelsFileSize - 1] == '\n') {
        labelsData[labelsFileSize - 1] = '\0';
    }

    // Make sure we always have a terminating NULL char after the label file
    // contents.
    labelsData[labelsFileSize] = '\0';

    // Now go through the list of strings and cap if strings too long.
    for (size_t i = 0; i < numLines; i++) {
        size_t stringLen = strnlen(labelArray[i], LINE_MAX_LEN);
        if (stringLen >= LINE_MAX_LEN) {
            // Just insert capping NULL terminator to limit the string len.
            *(labelArray[i] + LINE_MAX_LEN + 1) = '\0';
        }
    }

    *labelsPtr = labelArray;
    *numLabelsPtr = numLines;
    *labelFileBuffer = labelsData;

    ret = true;

end:
    if (!ret) {
        freeLabels(labelArray, labelsData);
    }
    close(labelsFd);

    return ret;
}

/**
 * brief Main function
 */
int main(int argc, char** argv) {
    // Hardcode to use three image "color" channels (eg. RGB).
    const unsigned int CHANNELS = 3;

    // Name patterns for the temp file we will create.
    char CONV_INP_FILE_PATTERN[] = "/tmp/larod.in.test-XXXXXX";
    char CONV_OUT_FILE_PATTERN[] = "/tmp/larod.out.test-XXXXXX";

    bool ret = false;
    larodError* error = NULL;
    larodConnection* conn = NULL;
    larodTensor** inputTensors = NULL;
    size_t numInputs = 0;
    larodTensor** outputTensors = NULL;
    size_t numOutputs = 0;
    larodJobRequest* infReq = NULL;
    void* larodInputAddr = MAP_FAILED;
    void* larodOutputAddr = MAP_FAILED;
    int larodModelFd = -1;
    int larodInputFd = -1;
    int larodOutputFd = -1;
    char** labels = NULL; // This is the array of label strings. The label
                          // entries points into the large labelFileData buffer.
    size_t numLabels = 0; // Number of entries in the labels array.
    char* labelFileData =
        NULL; // Buffer holding the complete collection of label strings.
    args_t args;

    // Open the syslog to report messages for "accuracy_measure"
    openlog("accuracy_measure", LOG_PID|LOG_CONS, LOG_USER);

    syslog(LOG_INFO, "Starting ...");

    if (!parseArgs(argc, argv, &args)) {
        goto end;
    }

    larodModelFd = open(args.modelFile, O_RDONLY);
    if (larodModelFd < 0) {
        syslog(LOG_ERR, "Unable to open model file %s: %s", args.modelFile,
               strerror(errno));
        goto end;
    }

    syslog(LOG_INFO, "Setting up larod connection with device %s and model %s", args.deviceName,
           args.modelFile);
    larodModel* model = NULL;
    if (!setupLarod(args.deviceName, larodModelFd, &conn, &model)) {
        goto end;
    }

    syslog(LOG_INFO, "Creating temporary files and memmaps for inference input and "
           "output tensors");

    if (!createAndMapTmpFile(CONV_INP_FILE_PATTERN,
                             args.width * args.height * CHANNELS,
                             &larodInputAddr, &larodInputFd)) {
        goto end;
    }

    if (!createAndMapTmpFile(CONV_OUT_FILE_PATTERN, args.outputBytes,
                             &larodOutputAddr, &larodOutputFd)) {
        goto end;
    }

    inputTensors = larodCreateModelInputs(model, &numInputs, &error);
    if (!inputTensors) {
        syslog(LOG_ERR, "Failed retrieving input tensors: %s", error->msg);
        goto end;
    }
    // This app only supports 1 input tensor right now.
    if (numInputs != 1) {
        syslog(LOG_ERR, "Model has %zu inputs, app only supports 1 input tensor.",
               numInputs);
        goto end;
    }
    if (!larodSetTensorFd(inputTensors[0], larodInputFd, &error)) {
        syslog(LOG_ERR, "Failed setting input tensor fd: %s", error->msg);
        goto end;
    }

    outputTensors = larodCreateModelOutputs(model, &numOutputs, &error);
    if (!outputTensors) {
        syslog(LOG_ERR, "Failed retrieving output tensors: %s", error->msg);
        goto end;
    }
    // This app only supports 1 output tensor right now.
    if (numOutputs != 1) {
        syslog(LOG_ERR, "Model has %zu outputs, app only supports 1 output tensor.",
               numOutputs);
        goto end;
    }
    if (!larodSetTensorFd(outputTensors[0], larodOutputFd, &error)) {
        syslog(LOG_ERR, "Failed setting output tensor fd: %s", error->msg);
        goto end;
    }
    // App supports only one input/output tensor.
    infReq = larodCreateJobRequest(model, inputTensors, 1, outputTensors,
                                         1, NULL, &error);
    if (!infReq) {
        syslog(LOG_ERR, "Failed creating inference request: %s", error->msg);
        goto end;
    }

    if (args.labelsFile) {
        if (!parseLabels(&labels, &labelFileData, args.labelsFile,
                         &numLabels)) {
            syslog(LOG_ERR, "Failed creating parsing labels file");
            goto end;
        }
    }

    /* make arrays of ground truths */
    int ground_truth[50000];
    FILE* file = fopen(args.annotationsFile, "r");
    if (file == NULL) {
        syslog(LOG_ERR, "Error : Failed to open annotations file: %s\n", strerror(errno));

        return 1;
    }
    char line[256];
    int b = 0;
    while (fgets(line, sizeof(line), file)) {

        /* note that fgets don't strip the terminating \n, checking its
        presence would allow to handle lines longer that sizeof(line) */
        // syslog(LOG_INFO, "element in each line of text file %s", line);
        //ground_truth[b] = atoi(line);
        sscanf(line, "%d", &ground_truth[b]);
        ground_truth[b] += 1;
        if (b<10) {
            // printf("%3d: %s\n", ground_truth[b], line);
        }
        b += 1;
    }
    fclose(file);
    int top1[N_IMAGES] = {0};
    int sum_top1 = 0;
    int sum_top5 = 0;

    int top5[N_IMAGES] = {0};
    float avg_top1;
    float avg_top5;

    for (size_t count = 1; count <= N_IMAGES; count++) {
        char img_name[50];
        snprintf(img_name, 50, "/var/spool/storage/SD_DISK/imagenet/%zu.bin", count);
        //printf("image name is %s\n", img_name);
        FILE *fp_input;
        fp_input = fopen(img_name, "rb");
        if (fp_input == NULL) {
            continue;
        }
        if (fread(larodInputAddr, 1, args.width * args.height * 3, fp_input) != args.width * args.height * 3) {
            syslog(LOG_ERR, "Unable to load image");
        }
        fclose(fp_input);

        if (!larodRunJob(conn, infReq, &error)) {
            syslog(LOG_ERR, "Unable to run inference on model %s: %s (%d)",
                args.modelFile, error->msg, error->code);
            goto end;
        }

        // Compute the most likely index.
        float maxProb = 0;
        uint8_t maxScore = 0;
        size_t maxIdx = 0;
        uint8_t* outputPtr = (uint8_t*) larodOutputAddr;
        int score_array_size = args.outputBytes;
        int score_array[score_array_size];
        float score_array_cv25[score_array_size];
        int score_array_indices[score_array_size];
        // The output has to be read differently depending on larod device.
        // In the case of the cv25, the space per element is 32 bytes and the
        // output is a float padded with zeros.
        // In the cases of artpec7, artpec8, and artpec9, the space per element is 1 byte
        // and the output is an uint8_t that has to be processed with softmax.
        // This part of the code can be improved by using better pointer casting,
        // subject to future changes.
        int spacePerElement;
        if (strcmp(args.deviceName, "ambarella-cvflow") == 0) {
            spacePerElement = 32;
            float score;
            for (size_t j = 0; j < args.outputBytes/spacePerElement; j++) {
                score = *((float*) (outputPtr + (j*spacePerElement)));
                score_array_cv25[j] = score;
                score_array_indices[j] = j;
                if (score > maxProb) {
                    maxProb = score;
                    maxIdx = j;
                }
        }
        } else {
            spacePerElement = 1;
            uint8_t score;
            for (size_t j = 0; j < args.outputBytes/spacePerElement; j++) {
                score = *((uint8_t*) (outputPtr + (j*spacePerElement)));
                score_array[j] = score;
                score_array_indices[j] = j;
                if (score > maxScore) {
                    maxScore = score;
                    maxIdx = j;
                }
            }

            float sum = 0.0;
            for (size_t j = 0; j < args.outputBytes/spacePerElement; j++) {
                score = *((uint8_t*) (outputPtr + (j*spacePerElement)));
                sum += exp(score - maxScore);
            }
            maxProb = 1/sum;
        }

        int l, m;
        int max, temp;

        // Partial selection sort, move k max elements to front
        if (strcmp(args.deviceName, "ambarella-cvflow") == 0) {

            for (l = 0; l < 5; l++) {

            max = l;
            // Find next max index
            for (m = l+1; m < score_array_size; m++) {
                if (score_array_cv25[m] > score_array_cv25[max]) {
                    max = m;
                }
            }
            // Swap numbers in input array
            temp = score_array_cv25[l];
            score_array_cv25[l] = score_array_cv25[max];
            score_array_cv25[max] = temp;
            // Swap indexes in tracking array
            temp = score_array_indices[l];
            score_array_indices[l] = score_array_indices[max];
            score_array_indices[max] = temp;
            }

        } else {

            for (l = 0; l < 5; l++) {

                max = l;
                // Find next max index
                for (m = l+1; m < score_array_size; m++) {
                    if (score_array[m] > score_array[max]) {
                        max = m;
                    }
                }
                // Swap numbers in input array
                temp = score_array[l];
                score_array[l] = score_array[max];
                score_array[max] = temp;
                // Swap indexes in tracking array
                temp = score_array_indices[l];
                score_array_indices[l] = score_array_indices[max];
                score_array_indices[max] = temp;
            }
        }
        int indices_top5[5];
        int ll;
        for (ll = 0; ll < 5; ll++) {
            indices_top5[ll] = score_array_indices[ll];
        }
        int mm;
        top5[count-1] = 0;
        for (mm = 0; mm < 5; mm++) {
            if (ground_truth[count-1] == indices_top5[mm]) {
                top5[count-1] = 1;
            }
        }
        if (top5[count-1] == 0) {
            syslog(LOG_INFO, "Image %zu is not top5, it's supposed to be %s, but it is classified as %s \n",
                count, labels[(size_t)ground_truth[count-1]], labels[maxIdx]);
            maxProb *= 100; //To have output int %
        }
        else {
            syslog(LOG_INFO, "Image %zu found in top5. \n", count);
        }
        if (labels) {
            if (maxIdx > numLabels) {
                syslog(LOG_INFO, "Top result: index %zu with score %.2f%% (index larger "
                    "than num items in labels file) statement 2", maxIdx, maxProb);
            }
        } else {
            syslog(LOG_INFO, "Top result: index %zu with score %.2f%% statement 3", maxIdx, maxProb);
        }
        if ((int) maxIdx == ground_truth[count-1]) {
            top1[count-1] = 1;
            syslog(LOG_INFO, "Image %zu found in top1. \n", count);
        } else {
            top1[count-1] = 0;
            syslog(LOG_INFO, "Image %zu is not top1, it's supposed to be %s, but it is classified as %s\n",
                count, labels[(size_t)ground_truth[count-1]], labels[maxIdx]);
        }

        sum_top1 += top1[count-1];
        sum_top5 += top5[count-1];
    }

    avg_top1 = (float)sum_top1/N_IMAGES*100;
    avg_top5 = (float)sum_top5/N_IMAGES*100;
    syslog(LOG_INFO, "\n");
    syslog(LOG_INFO, "RESULTS:\n");
    syslog(LOG_INFO, "top1 sum %d\n top5 sum %d\n top1 avg %.6f%% \n top 5 avg %.6f%% \n", sum_top1, sum_top5, avg_top1, avg_top5);
    syslog(LOG_INFO, "\n");

    ret = true;

end:
    // Only the model handle is released here. We count on larod service to
    // release the privately loaded model when the session is disconnected in
    // larodDisconnect().
    larodDestroyModel(&model);
    if (conn) {
        larodDisconnect(&conn, NULL);
    }
    if (larodModelFd >= 0) {
        close(larodModelFd);
    }
    if (larodInputAddr != MAP_FAILED) {
        munmap(larodInputAddr, args.width * args.height * CHANNELS);
    }
    if (larodInputFd >= 0) {
        close(larodInputFd);
    }
    if (larodOutputAddr != MAP_FAILED) {
        munmap(larodOutputAddr, args.outputBytes);
    }
    if (larodOutputFd >= 0) {
        close(larodOutputFd);
    }

    larodDestroyJobRequest(&infReq);
    larodDestroyTensors(conn, &inputTensors, numInputs, &error);
    larodDestroyTensors(conn, &outputTensors, numOutputs, &error);
    larodClearError(&error);

    if (labels) {
        freeLabels(labels, labelFileData);
    }

    return ret ? EXIT_SUCCESS : EXIT_FAILURE;
}
