# QCM-OCR

## Table of Contents
- [QCM-OCR](#qcm-ocr)
  - [Table of Contents](#table-of-contents)
  - [Install Requirements](#install-requirements)
  - [Run AMC via execution script](#run-amc-via-execution-script)
  - [Run Python OCR Script Manually](#run-python-ocr-script-manually)
  - [Run Unit Tests](#run-unit-tests)
  - [Run VisionAI Tests](#run-visionai-tests)
  - [Build AMC Manually](#build-amc-manually)
  - [Install AMC Manually](#install-amc-manually)
  - [Run AMC Manually](#run-amc-manually)


## Install Requirements
  ```bash
  ./install_requirements.sh
  ```

## Run AMC via execution script
  ```bash
  ./run.sh
  ```

## Run Python OCR Script Manually
* To run the script manually you need to fill the clean_data folder with your cr folder images

* The CROPPING argument must be set to 0 if the images are already cropped by hand to only fit the student numbers and 1 otherwise.
  Change line 3912 in the **auto-multiple-choice_1.5.2_sources/auto-multiple-choice-1.5.2/AMC-perl/AMC/Gui/Main.pm.in** file by commenting one of the calls as follows:

  ```pm
  system("python3 $python $source_folder $csv_file_path $client_secrets $source_folder 1");
  #system("python3 $python $clean_data $csv_file_path $client_secrets $source_folder 0");
  ```
* Run Commands:

  ```bash
  cd qcmocr/auto-multiple-choice_1.5.2_sources/auto-multiple-choice-1.5.2/AMC-perl/AMC/Gui/script-ocr
  ```
  ```bash
  python3 ocr_script.py SOURCE_FOLDER CSV_FILE_PATH CLIENT_SECRETS XML_PATH CROPPING
  ```

## Run Unit Tests

## Run VisionAI Tests

* Acess the test tests_visionai branch and run the following commands

  ```bash
  cd test_visionai
  python3 edit.py
  Python levenshtein-test.py
  ```

## Build AMC Manually
Should be in auto-multiple-choice-1.5.2 directory for building, installing or running:
  ```bash
  cd qcmocr/auto-multiple-choice_1.5.2_sources/auto-multiple-choice-1.5.2
  ```

  ```bash
  make version_files
  make
  ```
## Install AMC Manually
  ```bash
  sudo make install
  ```
## Run AMC Manually
  ```bash
  ./auto-multiple-choice
  ```

