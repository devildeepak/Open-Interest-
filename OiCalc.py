import streamlit as st
from PIL import Image
import pytesseract
import re
import matplotlib.pyplot as plt

# ✅ Define helper function first
def plot_pie_chart(put_oi, call_oi):
    labels = ['Put OI', 'Call OI']
    sizes = [put_oi, call_oi]
    colors = ['#4CAF50', '#2196F3']
    explode = (0.05, 0)  # highlight Put OI

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors,
           autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures pie is circular.
    return fig

# Streamlit UI
st.set_page_config(page_title="OI Analyzer", layout="centered")
st.title("📊 Option Chain OI Analyzer")

uploaded_file = st.file_uploader("Upload an option chain image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    if st.button("Analyze"):
        text = pytesseract.image_to_string(image)

        numbers = re.findall(r'\d[\d,]*', text)
        numbers = [int(num.replace(',', '')) for num in numbers]

        if len(numbers) < 3:
            st.error("Could not find enough numbers in the image. Try a clearer image.")
        else:
            puts = numbers[::3]
            calls = numbers[2::3]

            total_put_oi = sum(puts)
            total_call_oi = sum(calls)
            total_oi = total_put_oi + total_call_oi

            put_percent = (total_put_oi / total_oi) * 100
            call_percent = (total_call_oi / total_oi) * 100
            diff = total_put_oi - total_call_oi

            st.success("✅ Analysis Complete!")

            st.write(f"**Total Put OI:** {total_put_oi:,} ({put_percent:.2f}%)")
            st.write(f"**Total Call OI:** {total_call_oi:,} ({call_percent:.2f}%)")
            st.write(f"**Difference (Put - Call):** {diff:,}")

            # ✅ Call function to show chart
            fig = plot_pie_chart(total_put_oi, total_call_oi)
            st.pyplot(fig)
