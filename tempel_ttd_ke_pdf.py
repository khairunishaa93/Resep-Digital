import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io

st.set_page_config(page_title="Tempel TTD ke Resep", layout="centered")
st.title("📄✍️ Tempel Tanda Tangan ke Resep PDF")

# Upload file PDF dan tanda tangan PNG
pdf_file = st.file_uploader("📄 Upload File Resep (PDF)", type=["pdf"])
ttd_file = st.file_uploader("✍️ Upload Tanda Tangan Pasien (PNG)", type=["png"])

if pdf_file and ttd_file:
    if st.button("🔧 Tempel & Unduh PDF"):
        # Buka PDF dan ambil halaman pertama
        pdf = fitz.open(stream=pdf_file.read(), filetype="pdf")
        page = pdf[0]  # resep hanya 1 halaman

        # Buka tanda tangan PNG
        ttd_img = Image.open(ttd_file).convert("RGBA")
        buffer = io.BytesIO()
        ttd_img.save(buffer, format="PNG")

        # Sesuaikan posisi tempel (pojok kanan bawah kolom “PENERIMA OBAT”)
        # Ukuran tanda tangan 200 x 80 px, posisi kanan bawah A4
        rect = fitz.Rect(395, 740, 595, 820)  # (x1, y1, x2, y2)

        # Tempel gambar ke PDF
        page.insert_image(rect, stream=buffer.getvalue())

        # Simpan hasil ke output
        output = io.BytesIO()
        pdf.save(output)
        pdf.close()

        # Unduh hasil
        st.success("✅ Tanda tangan berhasil ditempel.")
        st.download_button(
            label="📥 Unduh PDF Bertanda Tangan",
            data=output.getvalue(),
            file_name="resep_dengan_ttd.pdf",
            mime="application/pdf"
        )
