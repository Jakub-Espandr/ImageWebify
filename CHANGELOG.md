# Changelog

## [0.0.1] – 2025-07-24

### Added
- Initial release of ImageWebify
- Batch conversion of JPG and PNG images to WebP
- Multi-file selection and conversion
- Output folder selection and auto-suggestion
- Adjustable quality slider (1–100)
- Adjustable max size (longest side, aspect ratio preserved)
- High-quality LANCZOS resampling
- In-app image preview window
- File size and estimated WebP size display
- Progress bar and status updates
- Custom font and icon support (fccTYPO-Regular, fccTYPO-Bold)
- Modern, user-friendly interface

### Improved
- Real-time update of estimated output size based on settings
- Automatic max size suggestion based on largest input image
- Output folder auto-fills to match input file location
- Multi-threaded conversion to keep UI responsive
- Error handling for missing files, output folders, or conversion issues

### Technical Details
- Built with Python and Tkinter (ttk)
- Uses Pillow for image processing and WebP conversion
- Threading for non-blocking UI during conversion
- Custom font and icon loading from assets directory

### Dependencies
- Pillow >= 8.0.0
- tkinter (Python standard library) 