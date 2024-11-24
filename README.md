<div align="center">
  <img src="assets/logo.png" alt="Tree Branch Tool Logo" width="200" height="200"/>

  # **Tree Branch Annotation and Prediction Tool**

  *A Comprehensive Tool for Annotating and Predicting Tree Branch Structures*

  [**Read the Paper**](https://doi.org/10.3390/f15091659) | [**Download Pre-trained Models**](models/) | [**Explore Dataset**](data/)
</div>

---

## **📖 Introduction**

This repository provides the software developed for the research paper:  
[**Automatic Method for Extracting Tree Branching Structures from a Single RGB Image**](https://doi.org/10.3390/f15091659) (**doi: 10.3390/f15091659**).

The tool offers:
- **Annotation Tool**: Manually annotate main trunks and primary branches.
- **Prediction Tool**: Predict tree branch structures using pre-trained models.
- **Dataset Builder**: Generate structured datasets for deep learning.
- **Pre-trained Models**: Access ready-to-use models trained for **400 epochs** and **1200 epochs**.
- **Sample Dataset**: Utilize copyright-free images and annotations for testing.

---

## **✨ Features**

✅ **Intuitive Annotation**  
Interactive tools to annotate tree branches with ease.

✅ **Deep Learning Integration**  
Load pre-trained models to predict branches directly from RGB images.

✅ **Dataset Export**  
Save annotations in XML format for training custom models.

✅ **Pre-trained Models & Dataset**  
Explore pre-trained models and a sample dataset included for testing.

---

## **🚀 Installation**

### Prerequisites
Make sure you have the following installed:
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

## **🖱️ Usage**

### Launch the GUI
Run the main script:
```bash
python PyUIPredict.py
```

### Annotation Workflow
1. **Open an Image**: Click **"Open File"** to load an image.  
2. **Annotate**:  
   - Left-click to annotate the **main trunk**.  
   - Use other mouse buttons to annotate **primary branches**.  
3. **Draw Lines**: Click **"Draw Line"** to connect annotated points.  
4. **Save Annotations**: Use **"Save Annotations"** to export to XML.

### Prediction Workflow
1. **Load a Model**: Click **"Select Model"** to load a pre-trained model.  
2. **Predict Branches**: Click **"Extract Features"** to generate predictions.  
3. **Visualize**: Review predicted branches directly on the canvas.

---

## **📁 Pre-trained Models**

Two pre-trained models are available:  
- **Model (400 Epochs)**: Balanced training for moderate accuracy.  
- **Model (1200 Epochs)**: Extended training for higher accuracy.  

Download models from the [models/](models/) directory.

---

## **📊 Sample Dataset**

The repository includes a sample dataset for testing:  
- Located in the [data/](data/) directory.  
- Includes sample images and corresponding XML annotations.

---

## **📂 Project Structure**

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

## **📜 Citing this Work**

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

## **📄 License**

This project is licensed under the MIT License. See the LICENSE file for details.
