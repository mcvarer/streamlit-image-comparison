import argparse
import glob
import os.path
from PIL import Image

import streamlit as st
from streamlit_image_comparison import image_comparison


st.set_page_config(
    page_title="Streamlit Multi-Image Comparison",
    page_icon="🔥",
    layout="centered",
    initial_sidebar_state="auto",
)

st.markdown(
    """
    <h2 style='text-align: center'>
    Streamlit Multi-Image Comparison
    </h2>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <p style='text-align: center'>
    <br />
    Follow me for more! <a href='https://github.com/mcvarer' target='_blank'><img src="https://img.icons8.com/fluency/48/000000/github.png" height="27"></a><a href='https://www.linkedin.com/in/mcanv/' target='_blank'><img src="https://img.icons8.com/fluency/48/000000/linkedin.png" height="30"></a> <a href='https://medium.com/@mcvarer' target='_blank'><img src="https://img.icons8.com/ios-filled/48/000000/medium-monogram.png" height="26"></a>
    </p>
    """,
    unsafe_allow_html=True,
)

st.write("##")

with st.form(key="Streamlit Multi-Image Comparison"):
    # image one inputs
    col1, col2 = st.columns([3, 1])
    with col2:
        img1_text = st.text_input("Image one text:", value="SLICE")
    # image two inputs
    col1, col2 = st.columns([3, 1])
    with col2:
        img2_text = st.text_input("Image two text:", value="SINGLE SHOT")

    # continious parameters
    col1, col2 = st.columns([1, 1])
    with col1:
        starting_position = st.slider(
            "Starting position of the slider:", min_value=0, max_value=100, value=50
        )
    with col2:
        width = st.slider(
            "Component width:", min_value=400, max_value=1000, value=700, step=100
        )

    # boolean parameters
    col1, col2, col3, col4 = st.columns([1, 3, 3, 3])
    with col2:
        show_labels = st.checkbox("Show labels", value=True)
    with col3:
        make_responsive = st.checkbox("Make responsive", value=True)
    with col4:
        in_memory = st.checkbox("In memory", value=True)

    # centered submit button
    col1, col2, col3 = st.columns([6, 4, 6])
    with col2:
        submit = st.form_submit_button("Update Render 🔥")


def parse_args():
    parser = argparse.ArgumentParser(description='Compare Model detected images')
    parser.add_argument('--slice-dir', default='results/slice', help='slice predicted images dir')
    parser.add_argument('--single-shot-dir', default='results/ss', help='single shot predicted images dir')
    parser.add_argument('--max-viz-images', default=15, help='max will be show images count')
    parser.add_argument('--type', default='png', help='png, jpeg, jpg')

    args = parser.parse_args()
    return args


def prepare_images(args):
    slice_dir = args.slice_dir
    single_shot_dir = args.single_shot_dir
    max_viz_images = args.max_viz_images
    file_type = args.type
    images_slices = sorted(glob.glob(os.path.join(slice_dir, f'*.{file_type}')))
    images_single_shot = sorted(glob.glob(os.path.join(single_shot_dir, f'*.{file_type}')))

    total_images = len(images_slices)
    if total_images >= max_viz_images:
        show_image_counts = max_viz_images
    else:
        show_image_counts = total_images

    pil_images_list = []
    if len(images_slices) == len(images_single_shot):
        for index, (img1_path, img2_path) in enumerate(zip(images_slices, images_single_shot)):

            if index == show_image_counts:
                break
            image1_pil = Image.open(img1_path)
            image2_pil = Image.open(img2_path)
            pil_images_list.append([image1_pil, image2_pil])

        return pil_images_list

    else:
        assert "Check your predicted images list"


def viz_imgs(img1, img2):
    static_component = image_comparison(
        img1=img1,
        img2=img2,
        label1=img1_text,
        label2=img2_text,
        width=width,
        starting_position=starting_position,
        show_labels=show_labels,
        make_responsive=make_responsive,
        in_memory=in_memory,
    )
    return static_component


if __name__ == '__main__':

    args = parse_args()
    images_pil_list = prepare_images(args)

    for images in images_pil_list:
        viz_imgs(img1=images[0], img2=images[1])

