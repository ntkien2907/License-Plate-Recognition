## License Plate Recognition


### Introduction
License plate detection is identifying the part of the car that is predicted to be the number plate. Recognition is identifying the values that make up the license plate. License plate detection and recognition is the technology that uses computer vision to detect and recognize a license plate from an input image of a car.
<p align='middle'><img src='./assets/applications.png' width=100% /></p>

---
### Setup
* Download Python 3.x [here](https://www.python.org/downloads/).
* Automatically install all dependencies from `requirements.txt`.
    ```
    pip install -r requirements.txt
    ```

---
### How to use
* Step 1: Download YOLO weight [here](https://www.mediafire.com/file/a38cal86u81z3xc/yolov3.weights/file) and put in `yolov3` folder.
* Step 2: Configure hyper-parameters in `config.py` file. There are many hyper-parameters which can be configured, but I recommend edit two parameters below:
    * `HOST`: Server domain.
    * `PORT`: Server port.
* Step 3: Start server.
    ```
    python app.py
    ```
<p align='middle'><img src='./assets/demo.png' width=100% /></p>

---
### References
1. [Nguyễn Chiến Thắng (2019). [Nhận diện biển số xe] Chương 1 – Phát hiện biển số xe bằng pretrain model YOLO.](https://www.miai.vn/2019/11/12/nhan-dien-bien-so-xe-chuong-1-phat-hien-bien-so-xe-bang-pretrain-model-yolo/)
2. [Aslan Ahmedov (2022). Automatic Number Plate Recognition.](https://www.kaggle.com/datasets/aslanahmedov/number-plate-detection)