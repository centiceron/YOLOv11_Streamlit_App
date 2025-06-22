#Import All the Required Libraries

import cv2
import streamlit as st
from pathlib import Path
import sys

from sympy.categories.baseclasses import Class
from tests import SOURCES_LIST
from ultralytics import YOLO
from PIL import Image

def app():
    #Get abs path of current file
    FILE = Path(__file__).resolve()

    #Get parent dir of current file
    ROOT = FILE.parent

    if ROOT not in sys.path:
        sys.path.append(str(ROOT))

    #Get relative path of root dir with respect to cwd
    ROOT = ROOT.relative_to(Path.cwd())

    #Sources
    IMAGE = "Image"
    VIDEO = "Video"

    SOURCES_LIST = [IMAGE,VIDEO]

    #Image Config
    DEFAULT_IMAGE = ".venv/images/img1.jpg"
    DEFAULT_DETECT_IMAGE = ".venv/images/detected_image1.jpg"

    #Model Configurations
    MODEL_DIR = ROOT/'weights'
    DETECTION_MODEL = MODEL_DIR/'yolo11n.pt'
    SEGMENTATION_MODEL = MODEL_DIR/'yolo11n-seg.pt'
    POSE_ESTIMATION_MODEL = MODEL_DIR/'yolo11n-pose.pt'
    CLASSIFIER_MODEL = MODEL_DIR/'yolo11n-cls.pt'

    #In case of custom detection model
    #DETECTION_MODEL = MODEL_DIR/'custom_model'

    #Page layout
    st.set_page_config(
        page_title="YOLOv11",
        page_icon="UNK"
    )

    st.header("Object Detection")

    #Sidebar
    st.sidebar.header("Model Configurations")

    #Choose model usage
    model = st.sidebar.radio("Task", ["Detection","Segmentation","Pose Estimation","Classification"])

    #Select confidence
    confidence_value = float(st.sidebar.slider("Select model confidence level", 20, 100, 40))/100

    #Selecting model type
    if model == "Detection":
        model_path = Path(DETECTION_MODEL)
    elif model == "Segmentation":
        model_path = Path(SEGMENTATION_MODEL)
    elif model == "Pose Estimation":
        model_path = Path(POSE_ESTIMATION_MODEL)
    elif model == "Classification":
        model_path = Path(CLASSIFIER_MODEL)

    #Load YOLO model
    try:
        model = YOLO(model_path)
    except Exception as e:
        st.error(f"Unable to load model. Check the path {model_path}")
        st.error(e)

    #Image/Video Config
    st.sidebar.header("Image / Video Configuration")
    source_radio = (st.sidebar.radio
                    ("Select Source", SOURCES_LIST))

    source_image = None
    if source_radio == IMAGE:
        source_image = (st.file_uploader
                       ("Upload an image", type=("jpg","png","jpeg")))

        col1, col2 = st.columns(2)
        with col1:
            try:
                if source_image is None:
                    default_image_path = str(DEFAULT_IMAGE)
                    default_image = Image.open(default_image_path)
                    st.image(default_image_path, caption = "Default Image", use_container_width=True)
                else:
                    uploaded_image = Image.open(source_image)
                    st.image(source_image, caption = "Uploaded Image", use_container_width=True)

            except Exception as e:
                st.error("Error occurred while opening image")
                st.error(e)

        with col2:
            try:
                if source_image is None:
                    default_detected_image_path = str(DEFAULT_DETECT_IMAGE)
                    default_detected_image = Image.open(default_detected_image_path)
                    st.image(default_detected_image_path, caption="Detected Image", use_container_width=True)
                else:
                    if st.sidebar.button("Detect"):
                        result = model.predict(uploaded_image, conf = confidence_value)
                        boxes = result[0].boxes
                        results_plotted = result[0].plot()[:,:,::-1]
                        st.image(results_plotted, caption="Detected Image", use_container_width=True)

                        try:
                            with st.expander("Detection Results"):
                                for box in boxes:
                                    st.write(box.data)
                        except Exception as e:
                            st.error(e)
            except Exception as e:
                st.error("Error occurred while opening the image")
                st.error(e)

    elif source_radio == VIDEO:
        source_video = (st.file_uploader
                        ("Upload a video file", type="mp4"))
        if source_video is not None:
            st.video(source_video)
        # source_video = st.sidebar.selectbox("Choose a video", VIDEOS_DICT.keys())
            if st.sidebar.button("Detect"):
                    try:
                        import tempfile
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
                            temp_file.write(source_video.read())
                            temp_file.close()

                            #Get path string
                            temp_video_path = temp_file.name

                        video_cap = cv2.VideoCapture(temp_video_path)
                        st_frame = st.empty()
                        while (video_cap.isOpened()):
                            success, image = video_cap.read()
                            if success:
                                image = cv2.resize(image,(720, int(720 * (9/16))))

                                #Predict the objects in the image using YOLOv11
                                result = model.predict(image, conf = confidence_value)

                                #Plot the detected objects of video
                                result_plotted = result[0].plot()
                                st_frame.image(result_plotted, caption="Detected Video", channels = "BGR", use_container_width=True)

                            else:
                                video_cap.release()
                                break
                    except Exception as e:
                        st.sidebar.error("Error occurred while opening the video" + str(e))

        else:
            print("Please upload a video file")