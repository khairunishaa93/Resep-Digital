import fitz  # PyMuPDF
from PIL import Image

def tempel_ttd_ke_pdf(pdf_path, ttd_path, output_path, posisi=(595, 456), ukuran=(100, 50)):
    # Buka file PDF
    pdf = fitz.open(pdf_path)
    page = pdf[0]  # halaman pertama

    # Buka gambar tanda tangan
    ttd_img = Image.open(ttd_path)
    ttd_img = ttd_img.resize(ukuran)  # resize agar tidak menutupi kolom lain

    # Simpan ke sementara (karena fitz butuh path file)
    ttd_temp_path = "temp_ttd.png"
    ttd_img.save(ttd_temp_path)

    # Hitung posisi berdasarkan koordinat kiri atas (x, y)
    x, y = posisi
    width, height = ukuran
    rect = fitz.Rect(x, y, x + width, y + height)

    # Sisipkan gambar ke halaman
    page.insert_image(rect, filename=ttd_temp_path)

    # Simpan file hasil
    pdf.save(output_path)
    pdf.close()
    print(f"Tanda tangan berhasil ditempel ke: {output_path}")
