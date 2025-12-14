# ===============================
# Solar Rooftop PV Pipeline Dockerfile
# ===============================

# 1️⃣ Base image (stable & evaluator-friendly)
FROM python:3.10-slim

# 2️⃣ Set working directory inside container
WORKDIR /app

# 3️⃣ Install system dependencies (OpenCV, PIL safety)
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# 4️⃣ Copy requirements first (Docker layer caching)
COPY requirements.txt .

# 5️⃣ Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 6️⃣ Copy entire project into container
COPY . .

# 7️⃣ Create input & output folders (safe default)
RUN mkdir -p /app/input /app/output

# 8️⃣ Default command (CLI help)
CMD ["python", "run_pipeline.py", "--help"]
