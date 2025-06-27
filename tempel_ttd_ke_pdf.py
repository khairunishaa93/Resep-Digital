import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import os

st.set_page_config(page_title="Gabung TTD ke PDF", layout="centered")
st.title("📎 Gabungkan Tanda Tangan Pasien ke Resep")

# Upload banyak file PDF dan PNG
pdf_files = st.file_uploader("📄 Upload File Resep (PDF)", type=["pdf"], accept_multiple_files=True)
ttd_files = st.file_uploader("✍️ Upload Tanda Tangan Pasien (PNG)", type=["png"], accept_multiple_files=True)

# Koordinat titik pojok kiri atas tanda tangan
x_default = 880
y_default = 1120
x = st.number_input("📍 Posisi X (horizontal)", value=x_default)
y = st.number_input("📍 Posisi Y (vertikal)", value=y_default)

if st.button("🚀 Proses dan Gabungkan"):
    if not pdf_files or not ttd_files:
        st.warning("Silakan upload file resep dan tanda tangan.")
    else:
        # Mapping tanda tangan berdasarkan nama (tanpa ekstensi)
        ttd_map = {os.path.splitext(ttd.name)[0].lower(): ttd for ttd in ttd_files}

        for pdf_file in pdf_files:
            nama = os.path.splitext(pdf_file.name)[0].lower()
            if nama in ttd_map:
                st.write(f"🛠️ Memproses: `{pdf_file.name}` + `{nama}.png`")

                # Buka PDF dan tanda tangan
                pdf = fitz.open(stream=pdf_file.read(), filetype="pdf")
                page = pdf[0]

                ttd_img = Image.open(ttd_map[nama]).convert("RGBA")
                buffer = io.BytesIO()
                ttd_img.save(buffer, format="PNG")

                # Ukuran tanda tangan (relatif kecil agar pas)
                rect = fitz.Rect(x, y, x + 150, y + 60)
                page.insert_image(rect, stream=buffer.getvalue())

                output = io.BytesIO()
                pdf.save(output)
                pdf.close()

                # Tombol download untuk masing-masing hasil
                st.download_button(
                    label=f"📥 Unduh {nama}_signed.pdf",
                    data=output.getvalue(),
                    file_name=f"{nama}_signed.pdf",
                    mime="application/pdf"
                )
            else:
                st.error(f"⚠️ Tidak ada tanda tangan untuk `{pdf_file.name}`")
