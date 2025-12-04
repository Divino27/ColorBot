import streamlit as st
import pandas as pd
import os
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="FutureColor Bot - Computer Expo",
    page_icon="🎉",
    layout="centered"
)

CSV_FILE = "futurecolor_cloud.csv"
ADMIN_PASSWORD = "amrita123@"   # <-- change if you want

# ---------------- CREATE CSV IF NOT EXISTS ----------------
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=["Name", "Age", "City", "Favorite Color", "Message"])
    df.to_csv(CSV_FILE, index=False)

# ---------------- SESSION STATE FOR PAGE NAVIGATION ----------------
if "page" not in st.session_state:
    st.session_state.page = "home"

def go_home():
    st.session_state.page = "home"

def go_form():
    st.session_state.page = "form"

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #ffe9d6, #fff4e3, #fbe4c2);
    background-size: cover;
}

.header-box {
    background: rgba(255,255,255,0.92);
    padding: 28px;
    border-radius: 25px;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.22);
    text-align: center;
    margin-bottom: 25px;
}

.top-image {
    width: 200px;
    margin-bottom: 10px;
    border-radius: 20px;
}

.robot-image {
    width: 120px;
    margin-top: -15px;
}

/* Certificate style */
.certificate-box {
    background: #fffdf5;
    border: 3px solid #f4c542;
    border-radius: 20px;
    padding: 20px;
    margin-top: 20px;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.15);
    text-align: center;
}

.certificate-title {
    font-size: 26px;
    font-weight: 800;
    color: #d48806;
    margin-bottom: 5px;
}

.certificate-name {
    font-size: 22px;
    font-weight: 700;
    color: #8A2BE2;
    margin: 8px 0;
}

.certificate-text {
    font-size: 16px;
    color: #333;
    margin-top: 5px;
}
</style>
""", unsafe_allow_html=True)

# Fun, kid-friendly images from the internet
fun_image = "https://yt3.ggpht.com/ytc/AIdro_lNE9F1qUp8GvAxWoWy67enscUnKgwEB5Rj00Fm35aa-w=s800-c-k-c0x00ffffff-no-rw"
robot_image = "https://cdn-icons-png.flaticon.com/512/4712/4712100.png"

# ---------------- FUTURE MESSAGES ----------------
messages = {
    "Red": (
        "🔥 You are bold, passionate, and full of unstoppable energy! "
        "Your future holds adventures, leadership, and powerful achievements."
    ),
    "Blue": (
        "🌊 Calm, intelligent, peaceful — your mind is your superpower! "
        "Great success in academics and creativity awaits you."
    ),
    "Green": (
        "🌿 Kind-hearted and caring — you bring harmony wherever you go. "
        "Your future will touch lives and inspire positivity."
    ),
    "Yellow": (
        "🌟 Bright, cheerful, creative — you make every place better! "
        "A fun, imaginative, and successful journey lies ahead."
    ),
    "Purple": (
        "🔮 Unique and imaginative — your ideas can change the world. "
        "Your future is full of innovation and brilliance."
    ),
    "Pink": (
        "💖 Loving and joyful — people feel happy around you. "
        "Your future will be full of friendships and heartwarming moments."
    ),
    "Black": (
        "⚫ Strong, focused, determined — you never give up! "
        "A powerful and successful path is waiting for you."
    ),
    "White": (
        "🤍 Pure, calm, peaceful — you bring comfort and clarity. "
        "A serene, graceful, and inspiring journey awaits."
    ),
}

# =========================================================
#                     HOME PAGE
# =========================================================
if st.session_state.page == "home":

    st.markdown(f"""
    <div class="header-box">
        <img src="{fun_image}" class="top-image">
        <h1 style="color:#8A2BE2; font-weight:900;">Welcome to the Computer Expo 2025 🎉</h1>
        <h2 style="color:#FF1493;">Amrita Vidyalayam, Kovur</h2>
        <h4 style="color:#333;">A Creative Project by V. Madhavan and Siddarth, 7A 💻✨</h4>
        <img src="{robot_image}" class="robot-image">
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.success("✨ Ready to discover your colourful future?")
    if st.button("🚀 Start Now"):
        go_form()

# =========================================================
#                     FORM PAGE
# =========================================================
if st.session_state.page == "form":

    st.header("🎨 Discover Your Colorful Future!")

    name = st.text_input("👤 Your Name")
    age = st.number_input("🎂 Your Age", min_value=1, max_value=100)
    city = st.text_input("🏙️ Your City")
    color = st.selectbox(
        "🎨 Your Favourite Color",
        ["Red", "Blue", "Green", "Yellow", "Purple", "Pink", "Black", "White"]
    )

    cert_pdf_bytes = None  # will hold PDF bytes for download

    if st.button("✨ Reveal My Future"):
        if name == "" or city == "":
            st.error("Please fill all fields!")
        else:
            msg = messages[color]
            st.success(f"Hi **{name}**, here is your colourful future:")
            st.info(msg)

            # Save to CSV
            df = pd.read_csv(CSV_FILE)
            new_row = {
                "Name": name,
                "Age": age,
                "City": city,
                "Favorite Color": color,
                "Message": msg
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(CSV_FILE, index=False)

            st.success("Your response has been saved! 📘")

            # --------- SIMPLE CERTIFICATE DISPLAY (ON SCREEN) ---------
            cert_html = f"""
            <div class="certificate-box">
                <div class="certificate-title">Certificate of Colourful Future ✨</div>
                <div class="certificate-text">This is to celebrate</div>
                <div class="certificate-name">{name}</div>
                <div class="certificate-text">
                    from {city}, who chose the colour <b>{color}</b>.<br>
                    According to the FutureColor Bot, your future is:
                </div>
                <div class="certificate-text" style="margin-top:10px;">
                    <i>{msg}</i>
                </div>
                <div class="certificate-text" style="margin-top:12px; font-size:14px; color:#777;">
                    You can download this certificate below or take a screenshot 📸 to keep it!
                </div>
            </div>
            """
            st.markdown(cert_html, unsafe_allow_html=True)

            # --------- GENERATE PDF CERTIFICATE IN MEMORY ---------
            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=A4)
            width, height = A4

            # Title
            c.setFont("Helvetica-Bold", 24)
            c.drawCentredString(width / 2, height - 100, "Certificate of Colourful Future")

            # Name
            c.setFont("Helvetica-Bold", 18)
            c.drawCentredString(width / 2, height - 150, f"Awarded to: {name}")

            # City & Color
            c.setFont("Helvetica", 14)
            c.drawCentredString(width / 2, height - 180, f"From: {city}")
            c.drawCentredString(width / 2, height - 205, f"Favourite Colour: {color}")

            # Message (wrap roughly into multiple lines)
            c.setFont("Helvetica-Oblique", 12)
            text_obj = c.beginText(80, height - 250)
            for line in msg.split(". "):
                text_obj.textLine(line.strip())
            c.drawText(text_obj)

            # Footer line
            c.setFont("Helvetica", 10)
            c.drawCentredString(width / 2, 80, "Generated at the Computer Expo 2025 - Amrita Vidyalayam, Kovur")

            c.showPage()
            c.save()
            buffer.seek(0)
            cert_pdf_bytes = buffer.getvalue()

            # Download button for this student's certificate
            st.download_button(
                label="📄 Download Your Certificate (PDF)",
                data=cert_pdf_bytes,
                file_name=f"{name.replace(' ', '_')}_FutureColor_Certificate.pdf",
                mime="application/pdf",
            )

    if st.button("🏠 Back to Home"):
        go_home()

# =========================================================
#                     ADMIN PANEL
# =========================================================
st.write("---")
st.header("🔒 Admin Access Only")

admin_pw = st.text_input("Enter admin password:", type="password")

if st.button("🔐 Login"):
    if admin_pw == ADMIN_PASSWORD:
        st.success("Admin login successful!")

        df = pd.read_csv(CSV_FILE)
        st.write("### 👀 All Responses")
        st.dataframe(df)

        # --------- COLOR POPULARITY CHART ---------
        if not df.empty:
            st.write("### 📊 Popular Colours")
            color_counts = df["Favorite Color"].value_counts().reindex(
                ["Red", "Blue", "Green", "Yellow", "Purple", "Pink", "Black", "White"],
                fill_value=0
            )
            st.bar_chart(color_counts)
        else:
            st.info("No data yet to show chart.")

        # Download CSV
        st.write("### 📥 Download Data")
        st.download_button(
            label="Download CSV Data",
            data=df.to_csv(index=False),
            file_name="futurecolor_data.csv",
            mime="text/csv",
        )
    else:
        st.error("❌ Incorrect password")

# =========================================================
#                     FOOTER
# =========================================================
st.write("---")
st.caption("© 2025 • Computer Expo • Amrita Vidyalayam • Made with ❤️ by Grade 7 Students")
