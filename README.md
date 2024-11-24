# Tree Branch Annotation and Prediction Tool

**A Comprehensive Tool for Annotating and Predicting Tree Branch Structures**

This repository provides the software developed for the research paper:  
[**Automatic Method for Extracting Tree Branching Structures from a Single RGB Image**](https://doi.org/10.3390/f15091659) (**doi: 10.3390/f15091659**).  

The tool offers functionalities for:
- Annotating tree branch structures interactively.
- Predicting tree branch structures using pre-trained deep learning models.
- Generating datasets for training branch prediction models.
- Accessing pre-trained models and sample datasets.

---

## Features

- **Annotation Tool**:  
  Annotate main trunks and primary branches interactively on RGB images.
- **Prediction Functionality**:  
  Use pre-trained deep learning models to predict tree branch structures.
- **Dataset Generation**:  
  Save annotations as structured XML files for dataset creation.
- **Pre-trained Models**:  
  Access models trained for **400 epochs** and **1200 epochs**.
- **Sample Dataset**:  
  Utilize copyright-free images and annotations for testing and reference.

---

## Installation

### Prerequisites

Ensure you have the following installed:
- Python 3.8+
- PyTorch
- PyQt5
- NumPy, OpenCV, Matplotlib, Pillow

### Clone the Repository

```bash
git clone https://github.com/your-username/tree-branch-annotation.git
cd tree-branch-annotation
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Usage

### Launch the GUI

Run the main script:

```bash
python PyUIPredict.py
```

### Annotation Workflow

1. **Open an Image**: Click **"Open File"** to load an image.
2. **Annotate**:
   - Left-click to annotate the main trunk.
   - Use other mouse buttons to annotate primary branches.
3. **Draw Lines**: Click **"Draw Line"** to connect annotated points.
4. **Save Annotations**: Use **"Save Annotations"** to save as an XML file.

### Prediction Workflow

1. **Load a Model**: Click **"Select Model"** to load a pre-trained model.
2. **Predict Branches**: Click **"Extract Features"** to generate predictions.
3. **Visualize**: Review predicted branches on the canvas.

---

## Pre-trained Models

Two pre-trained models are provided:
1. **Model (400 Epochs)**: Balanced training for moderate accuracy.
2. **Model (1200 Epochs)**: Extended training for higher accuracy.

Download models from the [models/](models/) directory or via links in this repository.

---

## Sample Dataset

The repository includes a small, copyright-free dataset for testing:
- Located in the [data/](data/) directory.
- Includes sample images and annotations.

---

## Project Structure

```plaintext
tree-branch-annotation/
│
├── data/                # Data directory (datasets, images, XML files)
│   ├── xml/             # Saved XML files
│   ├── png/             # Annotated images
│
├── models/              # Pre-trained models
│   ├── model_400.pth    # 400 epochs
│   ├── model_1200.pth   # 1200 epochs
│
├── PyUIPredict.py       # Main PyQt5-based application script
├── requirements.txt     # Python dependencies
├── README.md            # Documentation
```

---

## Citing this Work

If you use this tool in your research, please cite the following paper:

**Automatic Method for Extracting Tree Branching Structures from a Single RGB Image**  
[DOI: 10.3390/f15091659](https://doi.org/10.3390/f15091659)

```bibtex
@article{yourcitation,
  title={Automatic Method for Extracting Tree Branching Structures from a Single RGB Image},
  author={Your Authors},
  journal={Forests},
  volume={15},
  pages={1659},
  year={2023},
  publisher={MDPI}
}
```

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.
