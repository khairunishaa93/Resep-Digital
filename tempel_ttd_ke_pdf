import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io

st.set_page_config(page_title="Tempel TTD Pasien ke PDF", layout="centered")
st.title("🩺📄 Tempel Tanda Tangan Pasien ke Resep PDF")

# Upload file resep PDF dan tanda tangan PNG
pdf_file = st.file_uploader("📄 Upload File Resep (PDF)", type=["pdf"])
ttd_file = st.file_uploader("✍️ Upload Tanda Tangan Pasien (PNG)", type=["png"])

if pdf_file and ttd_file:
    if st.button("🖨️ Tempel & Unduh PDF"):
        # Buka PDF
        pdf = fitz.open(stream=pdf_file.read(), filetype="pdf")
        page = pdf[0]  # asumsinya resep hanya 1 halaman

        # Buka gambar tanda tangan
        ttd_img = Image.open(ttd_file).convert("RGBA")
        img_buffer = io.BytesIO()
        ttd_img.save(img_buffer, format="PNG")

        # Posisi tanda tangan (pojok kanan bawah)
        # Koordinat dalam satuan point (A4 = 595x842)
        posisi = fitz.Rect(450, 770, 570, 810)  # sesuaikan jika perlu

        # Tempelkan gambar ke PDF
        page.insert_image(posisi, stream=img_buffer.getvalue())

        # Simpan PDF ke memori
        output = io.BytesIO()
        pdf.save(output)
        pdf.close()

        # Tampilkan tombol download
        st.success("✅ Tanda tangan berhasil ditempel ke resep.")
        st.download_button(
            label="📥 Unduh PDF Final",
            data=output.getvalue(),
            file_name="resep_berttd.pdf",
            mime="application/pdf"
        )
