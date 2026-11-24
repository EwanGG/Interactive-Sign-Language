# Signova - Hand Landmark Prototype

## Purpose
Initial hand landmark data-processing prototype for Signova.

## Project Task
WBS 1.1.4 - Research Landmark Prototype

## Features
- Validation of 21 ordered hand landmarks.
- Wrist-centred coordinate normalisation.
- Hand-scale normalisation.
- Mean landmark distance comparison.
- Invalid scale detection.

## How to Run
python landmark_demo.py

## Testing
Synthetic data is used to test translation, uniform scaling,
changed landmark geometry and invalid scale rejection.

See test_results.txt for the execution results.

## Limitations
- No webcam integration.
- No rotation or perspective correction.
- No sign classification.
- No recognition accuracy evaluation.

## Next Steps
Integrate real MediaPipe landmark data and evaluate
the approach using selected sign language examples.

## Contributor
Nazanin Saedi

## AI Assistance
ChatGPT was used to support prototype development
and documentation.
