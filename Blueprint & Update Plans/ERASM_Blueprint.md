# Catalogue

This will hold a list of perquisites required before beginning the project.

## I | Prerequisites

#### Raw Data Source

Sigma Aldrich - https://www.sigmaaldrich.com/

#### Documents

1. Risk Assessment Template (RAT)   **||**      [docx]
2. International Chemical Hazard Codes (ICHC)   **||**      [docx][pdf]
3. Safety Data Sheets (SDS)     **||**      [pdf]
4. log_Blacklist   **||**      [txt]

#### Packages, libraries and other requirements

P1:
- OS 
- subprocess
- playwright
- selenium
- SDS_SU folder
- pdf reader

P2:
- pdf reader
- Log.txt file (store all accessed variables)

P3:
- IMPORT HCSS.PY (CUSTOM LIBRARY)
- Haz.csv file

P4:
- docx

P5:
- docx

PBeta:
- XYZ

PGamma:
- XYZ

## II | Structured planning

### 1. **PBeta** | *Hazard Code Sorting System (HCSS)*

### 2. **PGamma** | *ERAS Formatting*

### 3. **P1** | *SDS Extraction*

1. Playwright to access "Merck" (aka Sigma Aldrich) through chromium.
1. Playwright to search *chemical*.
1. Selenium to find SDS Download button *chemical*.
1. Download SDS to folder SDS_SU.
1. pdf reader to verify successful download

### 4. **P2** | *SDS Parsing*

### 5. **P3** | *Hazard tagging and Interpretation*

### 6. **P4** | *Hazard Entry*

### 7. **P5** | *Finishing Touches*

### 8. **P0Alpha** | *User input*

This will mainly comprise of 1 main input, which is the list of chemicals.

This will include an OS check, useful to verify the rest of the process, especially because current demands require communication between completely different operating systems.


## III. Basic Outline of each file (Can be used as comments later)

### 1. **P1** | *SDS Extraction*

SDS is grabbed using Playwright and Selenium and downloaded to the specified directory (SDS_SU). It ensures that the pdf was successfully downloaded by and verifying its readability.

If a corrupt file is detected, re-download will be queued.

Any error is this stage that continues to persist, will be sent to the log_Blacklist.txt file for review later.

### 2. **P2** | *SDS Parsing*

