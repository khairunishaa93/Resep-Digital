import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io

st.set_page_config(page_title="Tempel TTD ke Resep", layout="centered")
st.title("📄✍️ Tempel Tanda Tangan ke Resep PDF")

pdf_file = st.file_uploader("📄 Upload File Resep (PDF)", type=["pdf"])
ttd_file = st.file_uploader("✍️ Upload Tanda Tangan Pasien (PNG)", type=["png"])

if pdf_file and ttd_file:
    if st.button("🔧 Tempel & Unduh PDF"):
        pdf = fitz.open(stream=pdf_file.read(), filetype="pdf")
        page = pdf[0]

        st.write("🧭 Ukuran halaman PDF:", page.rect)

        ttd_img = Image.open(ttd_file).convert("RGBA")
        st.image(ttd_img, caption="Preview Tanda Tangan", width=200)

        buffer = io.BytesIO()
        ttd_img.save(buffer, format="PNG")

        # Debug: Coba tempel di tengah halaman dulu
        rect = fitz.Rect(395, 750, 595, 830)  # Tengah halaman

        page.insert_image(rect, stream=buffer.getvalue())

        output = io.BytesIO()
        pdf.save(output)
        pdf.close()

        st.success("✅ Tanda tangan berhasil ditempel (sementara di tengah halaman).")
        st.download_button(
            label="📥 Unduh PDF",
            data=output.getvalue(),
            file_name="resep_debug.pdf",
            mime="application/pdf"
        )
