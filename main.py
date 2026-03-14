import streamlit as st
from streamlit_image_carousel import image_carousel

import glob
import base64
from pathlib import Path
from time import sleep
import os

BASE_DIR = Path(__file__).parent

def img_to_b64(filename):
    path = BASE_DIR / "static" / filename
    data = path.read_bytes()
    b64 = base64.b64encode(data).decode()
    ext = Path(filename).suffix.lstrip(".")
    return f"data:image/{ext};base64,{b64}"

WELCOME_TEXT = "Happy Mother's Day (2026)!"

st.set_page_config(page_title=WELCOME_TEXT, layout="wide")

@st.cache_resource
def get_image_data():
    images = sorted(glob.glob(os.path.join(BASE_DIR, "static", "*.jpg")))
    static_data = [img_to_b64(image) for image in images]
    return static_data

def run_mothers_day():
    if not st.session_state.get("not_first_load"):
        st.session_state["not_first_load"] = True
        st.balloons()


    st.title("Happy Mother's Day (2026)!💜", text_alignment="center")

    image_data = get_image_data()



    with st.container(border=False, horizontal_alignment="center"):
        _ , mid, _ = st.columns([1, 4, 1], vertical_alignment="bottom")

        with mid:
            if not st.session_state.get("selected_image"):
                st.session_state["selected_image"] = image_data[0]

            st.image(st.session_state["selected_image"], use_container_width=True)



    img = image_carousel(image_data,
                        height=200,
                        key="selected_image")

    st.markdown("Dear Mum, hope you have a wonderful mother's day. I love you very much, Daniel x")


def validate_mum() -> bool:
    if st.session_state.get("validated"):
        return True
    else:
        quiz_mum()

@st.dialog(title="Checking this is Mum", dismissible=False)
def quiz_mum():
    ans = st.text_input("What is the first name of your favourite child?")

    if not ans.strip():
        st.write(ans.lower())
    elif ans.lower().startswith("catrin"):
        st.warning("No. The other one!")
    elif ans.lower() == "daniel":
        st.success("Correct! Poor Catrin-Haf :(")
        sleep(1)
        st.session_state["validated"] = True
        st.rerun()
    else:
        st.error("Wrong!")

    def show_orchid():
        st.image(img_to_b64(r"orchid.png"), width=200)

    with st.container(border=False, horizontal_alignment="center"):
        show_orchid()

def main():
    if validate_mum():
        run_mothers_day()

if __name__ == "__main__":
    main()