import streamlit as  st
import cv2
from cmath import inf
import numpy as np
import matplotlib.pyplot  as plt
def image_analyser(im):
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        dims = img.shape
        width = dims[1]
        height = dims[0]
        w_control = width // 100
        h_control = height // 100

        all_pixels = 0
        precoded_pixels = {(255, 255, 255): ["white", 0], (0, 0, 0): ["black", 0], (255, 0, 0): ["blue", 0],
                           (0, 255, 0): ["green", 0], (0, 0, 255): ["red", 0], (255, 244, 0): ["yellow", 0], (105, 245, 195): ["cyan", 0], }

        def matched_pixel(pixel):
            filter = float(inf)
            matched = ()
            for color in precoded_pixels:
                dif = abs(pixel[0] - color[0]) + abs(pixel[1] - color[1]) + abs(pixel[2] - color[2])
                if dif < filter:
                    filter = dif
                    matched = color

            return matched

        for i, rows in enumerate(img):
            if i % h_control:
                continue

            for j, pixel in enumerate(rows):
                if j % w_control:
                    continue

                # line to count all the pixels
                all_pixels += 1

                matched = matched_pixel(pixel)
                precoded_pixels[matched][1] += 1

        # loop for printing the percentage
        colors = []
        percentenges = []

        for color in precoded_pixels:
            name = precoded_pixels[color][0]
            occurences = precoded_pixels[color][1]
            percentenge = (occurences * 100) / all_pixels
            percentenge = round(percentenge, 1)
            if percentenge == 0:
                continue
            colors.append(name)
            percentenges.append(percentenge)
            print(f"{name}: {percentenge:.2f}%")
        return({"c" :colors, "p": percentenges})
        




st.set_page_config(layout="wide", page_title="Image color explorer")

st.write("## Explore the colos of your image")

col1, col2 = st.columns(2)
my_upload = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
click = st.sidebar.button("analyse image")



if my_upload is not None:#checking if an image is uploaded

    #read image
    file_bytes = my_upload.read()
    #convert it to a numpy array
    nparr = np.frombuffer(file_bytes, np.uint8)
    #transform numpy array to image in color mode 
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # Display the image using streamlit
    col1.image(img, channels="BGR", width=300)



    if click:# if the analyse button is clicked
        data_dic = image_analyser(nparr)
        print(data_dic)

        labels = data_dic["c"]

        sizes = data_dic["p"]  # Added a zero-size for Cyan

        # Plotting
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=labels)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Display pie chart using Streamlit
        col2.pyplot(fig)
