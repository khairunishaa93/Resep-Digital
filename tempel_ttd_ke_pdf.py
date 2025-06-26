import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io

st.set_page_config(page_title="Debug Tempel TTD", layout="centered")
st.title("🧪 Debug Posisi Tanda Tangan")

pdf_file = st.file_uploader("📄 Upload Resep (PDF)", type=["pdf"])
ttd_file = st.file_uploader("✍️ Upload Tanda Tangan (PNG)", type=["png"])

if pdf_file and ttd_file:
    x = st.slider("📍 Geser Horizontal (X)", 0, 595, 395)
    y = st.slider("📍 Geser Vertikal (Y)", 0, 842, 750)

    if st.button("🔧 Tempel & Lihat PDF"):
        pdf = fitz.open(stream=pdf_file.read(), filetype="pdf")
        page = pdf[0]

        ttd_img = Image.open(ttd_file).convert("RGBA")
        st.image(ttd_img, caption="🖼️ Preview Tanda Tangan", width=200)

        buffer = io.BytesIO()
        ttd_img.save(buffer, format="PNG")

        # Tempel tanda tangan sesuai slider
        rect = fitz.Rect(x, y, x + 200, y + 80)
        page.insert_image(rect, stream=buffer.getvalue())

        output = io.BytesIO()
        pdf.save(output)
        pdf.close()

        st.success("✅ PDF berhasil dibuat dengan posisi kustom.")
        st.download_button(
            label="📥 Unduh PDF",
            data=output.getvalue(),
            file_name="resep_debug.pdf",
            mime="application/pdf"
        )
