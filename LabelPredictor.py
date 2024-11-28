import copy
import os
import numpy as np
from xml.dom import minidom
import torch
import cv2
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from datetime import datetime
from bottleneck_transformer_pytorch import BottleStack
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PIL import Image
from torchvision import transforms

# Global variables for application state
annotation_flag = 0  # flag for annotation mode
main_branch_x = []  # X-coordinates of main branch points
main_branch_y = []  # Y-coordinates of main branch points
sub_branch_x = []  # X-coordinates of sub-branch points
sub_branch_y = []  # Y-coordinates of sub-branch points
main_branch_points = []  # List of main branch points as tuples
sub_branch_points = []  # List of sub-branch points as tuples
saved_branch_points = []  # Saved sub-branch points for later use
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")  # Device selection

# Global variables for image size and file name
image_width = 0  # Width of the loaded image
image_height = 0  # Height of the loaded image
file_name = 'name'  # Default file name

# Environment variable setting
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


class Ui_MainWindow(QtWidgets.QMainWindow):
    """
    Main Window class for the application, responsible for UI setup and functionality.
    """

    def setupUi(self, MainWindow):
        # Set up the main window and central widget
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1130, 950)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Create a QLabel widget for displaying content
        self.widget = QtWidgets.QLabel(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 20, 800, 900))
        self.gridLayout = QtWidgets.QGridLayout(MainWindow)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_2.setObjectName("gridLayout_2")

        # Button for opening files
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(900, 200, 160, 30))
        self.pushButton.setObjectName("pushButton")

        # Frame for content display
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(10, 20, 800, 900))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        # Frame for annotation tools
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setGeometry(QtCore.QRect(880, 270, 200, 200))
        self.frame_3.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        QLabel('\n' + '  Annotation Tools', self.frame_3)

        # Frame for automatic feature extraction tools
        self.frame_4 = QtWidgets.QFrame(self.centralwidget)
        self.frame_4.setGeometry(QtCore.QRect(880, 550, 200, 200))
        self.frame_4.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        QLabel('\n' + '  Automatic Extraction Tools', self.frame_4)

        # Layout for the display frame
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_3.setObjectName("gridLayout_3")


        # Set up Matplotlib figure and canvas
        self.figure1, self.figaxes1 = plt.subplots()
        self.canvas1 = FigureCanvas(self.figure1)

        # Example of adding interaction points on the canvas
        point, = self.figaxes1.plot([0], [0])
        PointBuilder(point) # Initialize point builder

        # Add Matplotlib navigation toolbar
        self.toolbar1 = NavigationToolbar(self.canvas1, self.centralwidget)
        self.toolbar1.setMinimumSize(QtCore.QSize(0, 41))
        self.toolbar1.setMaximumSize(QtCore.QSize(16777215, 41))
        self.gridLayout_3.addWidget(self.toolbar1, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.canvas1, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame_2, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)

        # Widget for other layout elements
        self.layoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget_3.setGeometry(QtCore.QRect(22, 12, 214, 22))
        self.layoutWidget_3.setObjectName("layoutWidget_3")

        # Additional elements and controls can be defined here...
                # Frame for line drawing options
        self.frame_line_range_5 = QtWidgets.QFrame(self.centralwidget)
        self.frame_line_range_5.setGeometry(QtCore.QRect(850, 250, 259, 189))
        # self.frame_line_range_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_line_range_5.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_line_range_5.setObjectName("frame_line_range_5")


        self.layoutWidget_9 = QtWidgets.QWidget(self.frame_line_range_5)
        self.layoutWidget_9.setGeometry(QtCore.QRect(20, 10, 227, 53))
        self.layoutWidget_9.setObjectName("layoutWidget_9")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.layoutWidget_9)
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label_13 = QtWidgets.QLabel(self.layoutWidget_9)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_13.addWidget(self.label_13)

        self.pushButton_16 = QtWidgets.QPushButton(self.frame_line_range_5)
        self.pushButton_16.setGeometry(QtCore.QRect(50, 110, 160, 30))
        self.pushButton_16.setObjectName("pushButton_16")
        self.comboBox_5 = QtWidgets.QComboBox(self.frame_line_range_5)
        self.comboBox_5.setGeometry(QtCore.QRect(50, 60, 160, 25))
        self.comboBox_5.setObjectName("comboBox_5")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.pushButton_15 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_15.setGeometry(QtCore.QRect(900, 410, 160, 30))
        self.pushButton_15.setObjectName("pushButton_15")
        self.pushButton_17 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_17.setGeometry(QtCore.QRect(900, 615, 160, 30))
        self.pushButton_17.setObjectName("pushButton_17")
        self.pushButton_18 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_18.setGeometry(QtCore.QRect(900, 665, 160, 30))
        self.pushButton_18.setObjectName("pushButton_18")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 916, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton.clicked.connect(self.open_btn_fun)
        self.pushButton_16.clicked.connect(self.draw_line_fun)
        self.pushButton_15.clicked.connect(self.create_xml_test)
        self.pushButton_17.clicked.connect(self.load_model_fun)
        self.pushButton_18.clicked.connect(self.predict_fun)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", " "))
        self.pushButton.setText(_translate("MainWindow", "open_button"))
        self.pushButton_16.setText(_translate("MainWindow", "draw_button"))
        self.comboBox_5.setItemText(0, _translate("MainWindow", "Main Branch"))
        self.comboBox_5.setItemText(1, _translate("MainWindow", "Sub-Branch"))
        self.pushButton_15.setText(_translate("MainWindow", "save_button"))
        self.pushButton_17.setText(_translate("MainWindow", "model_selection"))
        self.pushButton_18.setText(_translate("MainWindow", "extract_button"))


    def open_btn_fun(self):
        """
        Open an image file and load it for annotation.
        """
        global main_branch_x , main_branch_y , sub_branch_x , sub_branch_y
        global main_branch_points, sub_branch_points, image_width, image_height, annotation_flag
        main_branch_points.clear()
        sub_branch_points.clear()
        main_branch_x.clear()
        main_branch_y.clear()
        saved_branch_points.clear()

        annotation_flag = 0
        image_width = 0
        image_height = 0
        print("Opening file...")

        fileName = self.open_image_file()
        if fileName:
            self.img = cv2.imread(fileName)
            size = self.img.shape
            image_width = size[1]
            image_height = size[0]
            self.figaxes1.clear()
            self.showimg2figaxes(self.img)

    def load_model_fun(self):
        """
        Load a pre-trained deep learning model.
        """
        model = self.open_model_file()
        if model:
            self.load_model = torch.load(model)
            self.load_model.to(device)
            print("Model loaded successfully.")

    def showimg2figaxes(self, img):
        """
        Display a loaded image on the Matplotlib canvas.
        """
        print("Displaying image...")
        b, g, r = cv2.split(img)
        imgret = cv2.merge([r, g, b])  # OpenCV uses BGR, Matplotlib uses RGB
        self.figaxes1.imshow(imgret)
        self.figaxes1.autoscale_view()
        self.figure1.canvas.draw()

    def open_image_file(self):
        """
        Open a file dialog to select an image.
        """
        global fname
        print("Loading image file...")
        fileName, filetype = QFileDialog.getOpenFileName(self, 'Select Image File', 'C:/Users/Administrator/conda_project/data4.0/pic',
                                                         'All Files (*);;jpg Files (*.jpg);;'
                                                         'png Files (*.png)')
        fname = str(fileName)
        print(fname)
        return fileName

    def open_model_file(self):
        """
        Open a file dialog to select a model file.
        """
        print("Selecting model file...")
        torch.cuda.empty_cache()
        modelName, filetype = QFileDialog.getOpenFileName(self, 'Select Model',
                                                          'E:/4.0/test4.2',
                                                          'All Files (*);')
        print(modelName)
        return modelName

    def draw_line_fun(self):
        """
        Draw a line connecting annotated points on the image.
        """
        self.openimg2 = self.img
        global main_branch_x, main_branch_y, sub_branch_x, sub_branch_y, annotation_flag, saved_branch_points

        if self.comboBox_5.currentText() == "Main Branch":
            # Draw line for the main branch
            plt.plot(main_branch_x, main_branch_y, color='r', linewidth=1, marker="o")
        else:
            # Draw line for the sub-branch
            plt.plot(sub_branch_x, sub_branch_y, color='r', linewidth=1, marker="o")
            saved_branch_points.append(copy.deepcopy(sub_branch_points))
            annotation_flag += 1
        self.showimg2figaxes(self.openimg2)

        # Clear temporary branch points
        sub_branch_x.clear()
        sub_branch_y.clear()
        sub_branch_points.clear()
        print("Annotation flag:", annotation_flag)

    def predict_fun(self):
        """
        Use the loaded deep learning model to predict branch annotations on the image.
        """
        img = Image.open(fname)
        trans = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
        ])
        img0_r = trans(img)
        img0_r = img0_r.unsqueeze(0)
        img0_r = img0_r.to(device)
        outputs1, outputs2 = self.load_model(img0_r)
        outputs1 = outputs1.squeeze(0)  # if cuda is true
        predict_1 = outputs1.tolist()
        outputs2 = outputs2.squeeze(0)  # if cuda is true
        predict_2 = outputs2.tolist()
        print(predict_1)
        print(predict_2)
        predict_1 = predict_1 + predict_2
        predict = []
        #     print(predict_1)
        for i in predict_1:
            if i < 0 or i > 1:
                i = 0
            predict.append(i)
        print(len(predict))
        predict[0:20] = [val * image_width for val in predict[0:20]]
        predict[20:40] = [val * image_height for val in predict[20:40]]
        print(len(predict))
        self.figaxes1.clear()
        plt.plot(predict[0:20], predict[20:40], marker="o", color='r', markersize=3)
        for i in range(40, 240, 10):
            predict[i:i + 5] = [val * image_width for val in predict[i:i + 5]]
            predict[i + 5:i + 10] = [val * image_height for val in predict[i + 5:i + 10]]
            min_len = 100000000
            for a, b in zip(predict[0:20], predict[20:40]):
                point_len = np.sqrt((predict[i] - a) * (predict[i] - a) + (predict[i + 5] - b) * (predict[i + 5] - b))
                if point_len < min_len:
                    min_len = point_len
            if predict[i:i + 5].count(0) < 1 and predict[i + 5:i + 10].count(0) < 1 and min_len < (10 * image_width) / 224:
                plt.plot(predict[i:i + 5], predict[i + 5:i + 10], marker="o", color='r', markersize=3)
        self.showimg2figaxes(self.img)
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        print("Prediction completed at：", formatted_time)

    def create_xml_test(self):
        """
        Save annotated points and lines as an XML file.
        """
        global main_branch_x, main_branch_y, image_width, image_height, main_branch_points, sub_branch_points, file_name, saved_branch_points

        # Generate a black background image
        width, height = 640, 480
        black_image = np.zeros((height, width, 3), dtype=np.uint8)
        cv2.imwrite('black_background.png', black_image)
        self.img = cv2.imread('black_background.png')
        print(image_width, image_height)
        self.img = cv2.resize(self.img, (image_width, image_height), interpolation=cv2.INTER_CUBIC)
        self.figaxes1.clear()
        plt.plot(main_branch_x, main_branch_y, color='w', linewidth=3, marker="o")

        for i in range(len(saved_branch_points)):
            plotX = []
            plotY = []
            for j in saved_branch_points[i]:
                plotX.append(j[0])
                plotY.append(j[1])
            plt.plot(plotX, plotY, color='w', linewidth=2, marker="o")

        plt.axis('off')
        self.showimg2figaxes(self.img)
        
        xml = minidom.Document()
        file = xml.createElement('file')
        xml.appendChild(file)
        file.setAttribute('name', fname)

        level0 = xml.createElement('level0')
        file.appendChild(level0)

        level1 = xml.createElement('level1')
        file.appendChild(level1)

        point = xml.createElement('point')
        level0.appendChild(point)
        p0 = xml.createTextNode(str(main_branch_points))
        point.appendChild(p0)

        branch = xml.createElement('branch0')
        level0.appendChild(branch)
        p0 = xml.createTextNode(str(main_branch_points))
        branch.appendChild(p0)

        point = xml.createElement('point')
        level1.appendChild(point)
        value = xml.createTextNode(str(saved_branch_points))
        point.appendChild(value)

        for i in range(len(saved_branch_points)):
            branch = xml.createElement('branch1')
            branch.setAttribute('num', str(i))
            level1.appendChild(branch)
            value = xml.createTextNode(str(saved_branch_points[i]))
            branch.appendChild(value)

        parent_path = os.path.dirname(fname)
        file_name = os.path.split(fname)[-1]
        name = []
        for i in file_name:
            name.append(i)
            if i == '.':
                break
        name.remove('.')
        savename = ''.join(name)
        if not os.path.exists('./data/xml'):
            os.makedirs('./data/xml')
        if not os.path.exists('./data/png'):
            os.makedirs('./data/png')
        f = open('./data/xml/xml_' + savename + ".xml", 'w')
        plt.savefig('./data/png/png_' + savename, bbox_inches='tight', pad_inches=0)

        image = cv2.imread('./data/png/png_' + savename + '.png', cv2.IMREAD_UNCHANGED)
        
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        _, binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
        cv2.imwrite('./data/png/png_' + savename + '.png', binary_image)

        f.write(xml.toprettyxml())
        f.close()
        print(fname)

class PointBuilder:
    """
    Class for handling interactive point annotation on the Matplotlib canvas.
    """
    def __init__(self, point):
        """
        Initialize the PointBuilder.

        :param point: The Matplotlib line object representing the annotated points.
        """
        self.point = point
        self.xs = list(point.get_xdata()) # X-coordinates of annotated points
        self.ys = list(point.get_ydata()) # Y-coordinates of annotated points
        self.cid = point.figure.canvas.mpl_connect('button_press_event', self) # Connect mouse click events

    def __call__(self, event):
        """
        Handle mouse click events for point annotation.

        :param event: The Matplotlib mouse event.
        """
        global main_branch_points, sub_branch_points, main_branch_x, main_branch_y, sub_branch_x, sub_branch_y

        # Determine point size based on the mouse button used
        if event.button == 1:
            pointsize = 30
        else:
            pointsize = 10
        
        # Ignore clicks outside the axes
        if event.inaxes != self.point.axes: return

        # Add the point to the list of annotations
        self.xs.append(event.xdata)
        self.ys.append(event.ydata)
        self.point.set_data(self.xs, self.ys)

        # Draw the point on the canvas
        plt.scatter(event.xdata, event.ydata, color='#00CED1', s=pointsize)
        self.point.figure.canvas.draw()

        # Store the point in the appropriate global list
        if event.button == 1: # Left mouse button for main branch
            main_branch_points.append((event.xdata, event.ydata))
            main_branch_x.append(event.xdata)
            main_branch_y.append(event.ydata)
        else:  # Other mouse buttons for sub-branch
            sub_branch_points.append((event.xdata, event.ydata))
            sub_branch_x.append(event.xdata)
            sub_branch_y.append(event.ydata)


def forward(self, x):
    """
    Forward pass for the deep learning model.

    :param x: Input tensor.
    :return: Two output tensors corresponding to different prediction tasks.
    """
    x = self.conv1(x)
    x = self.bn1(x)
    x = self.relu(x)
    x = self.maxpool(x)

    x = self.layer1(x)
    x = self.layer2(x)
    x = self.layer3(x)
    x = self.layer4(x)

    # Optionally include bottleneck transformer stack (commented out)
    # x = self.bottleStack(x)
    x = self.avgpool(x)
    x = torch.flatten(x, 1)
    x1 = self.fc(x) # Output for the first prediction task
    x2 = self.fc1(x) # Output for the second prediction task
    return x1, x2


if __name__ == "__main__":
    """
    Main entry point for the application. Initializes and runs the PyQt5 application.
    """
    import sys

    # Initialize the application
    app = QtWidgets.QApplication(sys.argv)

    # Create and configure the main window
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    # Execute the application
    sys.exit(app.exec_())
