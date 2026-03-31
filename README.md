# Football Match Winner Prediction MLOps Project

This project implements an MLOps pipeline for predicting football match winners using machine learning.

## Project Structure

- `data/`: Raw and processed data
- `src/`: Source code for data processing, training, and evaluation
- `api/`: FastAPI application for serving predictions
- `models/`: Trained model artifacts
- `reports/`: Evaluation reports and metrics
- `params.yaml`: Model hyperparameters
- `dvc.yaml`: DVC pipeline configuration
- `requirements.txt`: Python dependencies

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Initialize DVC: `dvc init`
3. Initialize Git: `git init`

## Usage

Run the DVC pipeline: `dvc repro`