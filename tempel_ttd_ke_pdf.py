import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io

st.set_page_config(page_title="Debug Tempel TTD", layout="centered")
st.title("🧪 Debug Tempel TTD ke Resep")

pdf_file = st.file_uploader("📄 Upload Resep (PDF)", type=["pdf"])
ttd_file = st.file_uploader("✍️ Upload Tanda Tangan (PNG)", type=["png"])

# Posisi final hasil slider kemarin
final_x = 600
final_y = 1070
ttd_width = 100
ttd_height = 50

if pdf_file and ttd_file:
    st.markdown("📌 Posisi tanda tangan otomatis ke kolom **PENERIMA OBAT** (kanan bawah).")

    if st.button("📌 Tempel & Lihat Hasil"):
        # Buka file PDF dan ambil halaman pertama
        pdf = fitz.open(stream=pdf_file.read(), filetype="pdf")
        page = pdf[0]

        # Buka tanda tangan dan simpan ke buffer
        ttd_img = Image.open(ttd_file).convert("RGBA")
        st.image(ttd_img, caption="🖼️ Preview Tanda Tangan", width=200)

        buffer = io.BytesIO()
        ttd_img.save(buffer, format="PNG")

        # Tempel tanda tangan ke posisi akhir yang pas
        rect = fitz.Rect(final_x, final_y, final_x + ttd_width, final_y + ttd_height)
        page.insert_image(rect, stream=buffer.getvalue())

        # Simpan hasil ke output
        output = io.BytesIO()
        pdf.save(output)
        pdf.close()

        st.success("✅ PDF berhasil dibuat dan tanda tangan sudah pas.")
        st.download_button(
            label="📥 Unduh PDF",
            data=output.getvalue(),
            file_name="resep_ttd_final.pdf",
            mime="application/pdf"
        )
