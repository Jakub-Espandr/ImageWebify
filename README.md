<p align="center">
  <a href="https://i.ibb.co/GQsDVPR0/icon.png">
    <img src="https://i.ibb.co/GQsDVPR0/icon.png" alt="ImageWebify Logo" width="250"/>
  </a>
</p>

<h1 align="center">ImageWebify – Batch JPG/PNG to WebP Converter</h1>
<p align="center"><em>(by Jakub Ešpandr)</em></p>

## Overview

**ImageWebify** is a user-friendly batch converter for JPG and PNG images to the modern, efficient WebP format. It features quality and size controls, custom fonts, and a modern interface. Perfect for photographers, web developers, and anyone who needs to optimize images for the web.

---

## ✨ Features

- **Batch Conversion**
  - Select multiple JPG/PNG images at once
  - Convert only selected files from the list
- **Image Processing**
  - JPG/PNG to WebP conversion
  - Adjustable quality slider (1–100)
  - Adjustable max size (longest side, with aspect ratio preserved)
  - High-quality LANCZOS resampling
- **Preview & Info**
  - Quick image preview in-app
  - File size and estimated WebP size display
- **Modern UI**
  - Custom fonts and icons
  - Progress bar and status updates

---

## 📦 Requirements

- Python 3.7+
- [Pillow](https://python-pillow.org/) – Image processing library
- Tkinter (usually included with Python)
- Custom fonts (included in `assets/fonts/`)

---

## 🚀 Installation

```bash
git clone https://github.com/Jakub-Espandr/ImageWebify.git
cd ImageWebify
```

Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

Install required Python libraries:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

---

## 🛠️ Usage

1. **Add Images**: Click "Browse Files" to select JPG/PNG images.
2. **Select Output Folder**: Choose where converted images will be saved.
3. **Adjust Settings**: Set quality and max size as desired.
4. **Preview**: Select a file and click "Preview" to see it in-app.
5. **Convert**: Select one or more files in the list and click "Convert Selected Images".
6. **Monitor Progress**: Watch the progress bar and status updates.

---

## 📁 Project Structure

```
ImageWebify/
├── main.py                  # Entry point
├── assets/
│   ├── icons/              # Application icons (icon.png)
│   └── fonts/              # Custom fonts (fccTYPO-Regular.ttf, fccTYPO-Bold.ttf)
├── requirements.txt        # Dependencies
└── README.md               # This file
```

---

## 🔐 License

This project is licensed under the **Non-Commercial Public License (NCPL v1.0)**  
© 2025 Jakub Ešpandr - Born4FLight, FlyCamCzech

See the [LICENSE](https://github.com/Jakub-Espandr/imagewebify/raw/main/LICENSE) file for full terms.

---

## 🙏 Acknowledgments

- Built with ❤️ using Tkinter, Pillow, and open-source libraries