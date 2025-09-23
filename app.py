import streamlit as st  
import qrcode 
from io import BytesIO
import re

def validate_upi_id(upi_id):
    # UPI ID pattern: username/mobile@upi
    upi_pattern = r'^[\w\.\-]+@[\w\-]+$'
    if not re.match(upi_pattern, upi_id):
        return False
    # Check if UPI handle is valid
    valid_upi_handles = ['upi', 'okicici', 'okaxis', 'okhdfcbank', 'okbizaxis', 'oksbi', 'paytm', 'apl',]
    upi_handle = upi_id.split('@')[1].lower()
    return upi_handle in valid_upi_handles

def generate_upi_qrcode(upi_id,amount=""):
    upi_url = f"upi://pay?pa={upi_id}"
    if amount.strip():
        upi_url += f"&am={amount}&cu=INR"
    qr = qrcode.make(upi_url)

    buf = BytesIO()
    qr.save(buf,format="PNG")
    byte_im = buf.getvalue()
    return byte_im, upi_url

# front_end Work

st.set_page_config(page_title="PayQR",page_icon="",layout="centered")
st.title("PayQR")
st.write("Generate a UPI code that Works with **GPay,Phonepe,Paytm** etc")
upi_id = st.text_input("Enter the UPI Id")
amount = st.text_input("Enter the Amount(Optional)")

if st.button("Generate QR Code"):
    if not upi_id.strip():
        st.warning("Please Enter the UPI ID Before Generating QR")
    elif not validate_upi_id(upi_id):
        st.error("Invalid UPI ID format. Please enter a valid UPI ID (e.g., username@upi)")
    else:
        try:
            byte_im,upi_url=generate_upi_qrcode(upi_id,amount)
            st.image(byte_im,caption="Scan this QR code to Pay")

            st.download_button(
                label="Download QR Code",
                data = byte_im,
                file_name = f"{upi_id}_qr.png",
                mime = "image/png"
            )
            st.success("QR Code Generated Successfully")
            st.code(upi_url,language="text")
        except Exception as e:
            st.error(f"{str(e)}")