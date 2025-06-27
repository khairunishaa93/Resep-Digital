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
x_default = 655
y_default = 456
x = st.number_input("📍 Posisi X (horizontal)", value=x_default)
y = st.number_input("📍 Posisi Y (vertikal)", value=y_default)

# Ukuran tanda tangan (dalam piksel PDF)
width = st.number_input("📏 Lebar Tanda Tangan (px)", value=150)
height = st.number_input("📐 Tinggi Tanda Tangan (px)", value=60)

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

                # Baca dan resize gambar tanda tangan
                ttd_img = Image.open(ttd_map[nama]).convert("RGBA")
                resized_ttd = ttd_img.resize((width, height))  # resize ke ukuran yang diinginkan

                buffer = io.BytesIO()
                resized_ttd.save(buffer, format="PNG")

                # Sisipkan ke PDF
                rect = fitz.Rect(x, y, x + width, y + height)
                page.insert_image(rect, stream=buffer.getvalue())

                # Simpan hasil ke memory
                output = io.BytesIO()
                pdf.save(output)
                pdf.close()

                # Tombol download hasil
                st.download_button(
                    label=f"📥 Unduh {nama}_signed.pdf",
                    data=output.getvalue(),
                    file_name=f"{nama}_signed.pdf",
                    mime="application/pdf"
                )
            else:
                st.error(f"⚠️ Tidak ada tanda tangan untuk `{pdf_file.name}`")
