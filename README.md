🏠 Solar Rooftop PV Detection Pipeline
SOLAR ROOFTOP PV DETECTION PIPELINE

TEAM NAME: NEURAL NOMADS
TEAM MEMBERS:
1) VISHAL VETCHA
2) JYOTSNA MALLENA
3) REZIE PAUL ILAVARAPU

This repository provides a production-grade, end-to-end Python pipeline for detecting rooftop solar photovoltaic (PV) installations from satellite imagery using deep learning.
The pipeline is designed to be robust, auditable, and evaluator-friendly, fully aligned with the problem statement requirements.

WHAT THIS PIPELINE DOES?

1) For each site provided via latitude and longitude, the pipeline:

2) Fetches high-resolution satellite imagery

3) Detects rooftop solar PV using a trained YOLOv8 segmentation model

4) Applies multi-zoom inference to handle scale mismatch

5) Classifies solar presence (present / not present)

6) Estimates PV panel area (m²) when detected

7) Generates explainability artifacts (overlay images)

8) Assigns a QC status (VERIFIABLE / NOT_VERIFIABLE)

9) Stores outputs as JSON and images

📂 Project Structure
```text
solar_rooftop_pv_pipeline/
│
├── run_pipeline.py          # Main CLI entrypoint (this is what you run)
├── requirements.txt
├── README.md
│
├── config/
│   ├── settings.yaml
│   └── model_config.yaml
│
├── models/
│   └── solar_yolov8_seg.pt  # Trained YOLOv8 segmentation model
│
├── input/                   # (Optional) recommended location for input Excel
│
├── output/
│   ├── json/                # One JSON per sample_id
│   ├── overlays/            # Audit overlay images
│   └── logs/                # Execution logs
│
└── src/
|   ├── data/                # Excel loading, image fetching
|   ├── inference/           # Model, multi-zoom logic, detection
|   ├── qc/                  # QC rules
|   ├── utils/               # Helpers (geo, logging, image utils)
|   └── output/              # Output writer
| training_logs/
    |__training_metrics.csv

INPUT REQUIREMENTS
Excel File Format (.xlsx)

The pipeline expects an Excel file containing at least the following columns:

| Column Name | Description            |
| ----------- | ---------------------- |
| `sample_id` | Unique site identifier |
| `latitude`  | Latitude (WGS84)       |
| `longitude` | Longitude (WGS84)      |

✅ Additional columns (if present) are ignored.
❌ Rows with invalid latitude/longitude will raise an error.





⚙️ INSTALLATION AND PIPELINE RUNNING GUIDELINES 

WE HAVE PROVIDED TWO WAYS TO RUN THE PIPELINE
                            |__ Running with Docker
                            |__ Running the Pipeline (CLI Mode)(Command line interface)

**RUNNING THE PIPELINE WITH DOCKER (RECOMMENDED)**
**A pre-built Docker image is already available on Docker Hub.**

### Docker Image

Docker Image:
vishalvetcha/solar-rooftop-pv-pipeline:latest

**Docker Hub Repository:**  
vishalvetcha/solar-rooftop-pv-pipeline

**Image Tag:**  
latest

**FOLLOW THE GUIDELINES STEP BY STEP**

1) Step 1 — Pull the Docker Image

run this command:

docker pull vishalvetcha/solar-rooftop-pv-pipeline:latest

2) Step 2 — Run the Pipeline Using Docker
Mount:
A local folder containing your Excel input file
The repository’s output/ folder (results are written automatically)

run this command: 

docker run --rm \
  -v <REPLACE WITH PATH_TO_FOLDER_CONTAINING_EXCEL>:/app/input \
  -v $(pwd)/output:/app/output \
  vishalvetcha/solar-rooftop-pv-pipeline:latest \
  python run_pipeline.py --input /app/input/<REPLACE WITH YOUR_EXCEL_FILENAME>.xlsx

**IMPORTANT** 
1) Replace <REPLACE WITH PATH_TO_FOLDER_CONTAINING_EXCEL> with the folder containing your Excel file
2) Replace <REPLACE WITH YOUR_EXCEL_FILENAME> with the file name of the excel sheet

Example Command (JUST AN EXAMPLE-REFER THE GUIDELINES AND ABOVE COMMANDS FOR PROCEDURE)
docker run --rm \
  -v /home/user/data:/app/input \
  -v $(pwd)/output:/app/output \
  vishalvetcha/solar-rooftop-pv-pipeline:latest \
  python run_pipeline.py --input /app/input/sites.xlsx

Important Notes for Evaluators

The Excel file can be named anything
Just ensure the filename matches what you pass to --input
Outputs are always written to the repository’s output/ directory
No additional configuration is required

📂 **Output Location (Automatic)**

After execution, results will be available at:

output/
├── json/
├── overlays/
└── logs/


**RUNNING THE PIPELINE (CLI Mode)**

Step 1 — Install Python Dependencies
run this command on cli:

pip install -r requirements.txt

Step 2 — Run the Pipeline

python run_pipeline.py --input <COPY PASTE YOUR INPUT FILE PATH HERE>
 

EXAMPLE:
python run_pipeline.py --input input/sites.xlsx


1) Replace input/sites.xlsx with the actual path to your Excel file.

2) The input/ folder does not need to contain anything beforehand.

3) Outputs are written automatically to the output folder.

**IMPORTANT**
1) Replace <COPY PASTE YOUR INPUT FILE PATH HERE> with the folder containing your Excel file
📂 **Output Location (Automatic)**

After execution, results are saved to:

output/
├── json/        # Prediction JSON files
├── overlays/    # Audit overlay images
└── logs/        # Execution logs



**Training logs and metrics across epochs are provided under the `training_logs/` directory as a CSV file.**

**Prediction Files** (on training dataset provided)
Predictions on the training dataset are provided in both CSV and JSON formats under prediction_files/.

**QUALITY CONTROL LOGIC**
QC status is determined as follows:

| QC Status        | Meaning                                                |
| ---------------- | ------------------------------------------------------ |
| `VERIFIABLE`     | Clear detection or confident absence                   |
| `NOT_VERIFIABLE` | Low resolution, shadows, occlusion, or missing imagery |

**MODEL DETAILS**

Model: YOLOv8 Segmentation

Trained on rooftop solar datasets

Multi-zoom inference improves detection of small PV installations

Optimized for satellite imagery



**RECOMMENDED USAGE FOR EVALUATORS**

Preferred
Run via Docker

Alternative
Run via CLI if Docker is unavailable

Both produce identical outputs.


**Reproducibility & Robustness**

Version-locked dependencies
Externalized YAML configuration
No hard-coded paths
CLI-driven execution AND docker driven execution
Graceful handling of failures

**Notes for Evaluators**

No notebooks are required
No manual intervention needed
Outputs are deterministic and auditable
The pipeline prioritizes honest inference over false positives

**SUMMARY**
This repository delivers a complete, competition-ready solution for rooftop solar PV detection that is:

1) Accurate

2) Explainable

3) Robust to real-world imagery issues

4) Fully aligned with the evaluation requirements