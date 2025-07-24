import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
import os
from pathlib import Path
import threading
import sys

class ImageConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("ImageWebify")
        self.root.geometry("600x640")
        self.root.minsize(600, 640)
        self.root.resizable(True, True)
        self.set_application_icon()

        # Load custom fonts
        try:
            font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "fonts")
            self.regular_font = ("fccTYPO-Regular", 12)
            self.bold_font = ("fccTYPO-Bold", 12)
        except Exception as e:
            print(f"Warning: Could not load custom fonts: {e}")
            self.regular_font = ("Arial", 12)
            self.bold_font = ("Arial", 12)
        # Variables
        self.selected_files = []
        self.output_folder = tk.StringVar()
        self.quality = tk.IntVar(value=80)
        self.max_size = tk.IntVar(value=1920)
        self.preserve_aspect = True  # Always preserve aspect ratio
        
        self.setup_ui()
        
    def set_application_icon(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(current_dir, "assets", "icons")
            if sys.platform == "darwin":
                icon_file = os.path.join(icon_path, "icon.png")
                if os.path.exists(icon_file):
                    icon = tk.PhotoImage(file=icon_file)
                    self.root.iconphoto(True, icon)
            elif sys.platform == "win32":
                icon_file = os.path.join(icon_path, "icon.ico")
                if os.path.exists(icon_file):
                    self.root.iconbitmap(icon_file)
            else:
                icon_file = os.path.join(icon_path, "icon.png")
                if os.path.exists(icon_file):
                    icon = tk.PhotoImage(file=icon_file)
                    self.root.iconphoto(True, icon)
        except Exception as e:
            print(f"Error loading application icon: {str(e)}")

    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # File selection section
        ttk.Label(main_frame, text="Add Images to List:", font=self.bold_font).grid(
            row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 10)
        )
        
        ttk.Button(main_frame, text="Browse Files", command=self.browse_files, style="Custom.TButton").grid(
            row=1, column=0, sticky=tk.W, padx=(0, 10)
        )
        
        ttk.Button(main_frame, text="Clear Selection", command=self.clear_files, style="Custom.TButton").grid(
            row=1, column=1, sticky=tk.W
        )
        
        ttk.Button(main_frame, text="Preview", command=self.preview_selected_image, style="Custom.TButton").grid(
            row=1, column=2, sticky=tk.W, padx=(10, 0)
        )
        
        # File list
        self.file_listbox = tk.Listbox(main_frame, height=8, selectmode=tk.EXTENDED)
        self.file_listbox.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        self.file_listbox.bind('<<ListboxSelect>>', self.on_file_select)
        
        # Scrollbar for listbox
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        scrollbar.grid(row=2, column=3, sticky=(tk.N, tk.S), pady=(10, 0))
        self.file_listbox.config(yscrollcommand=scrollbar.set)
        
        # Instruction label
        ttk.Label(main_frame, text="💡 Select one or more files from the list above to convert (use Command ⌘ or Shift to multi-select on Mac, Ctrl or Shift on Windows)", 
                 font=self.regular_font, foreground="gray").grid(
            row=3, column=0, columnspan=3, sticky=tk.W, pady=(5, 0)
        )
        
        # Set up custom style for LabelFrame label (optional, may not work on all platforms)
        style = ttk.Style()
        try:
            style.configure("Custom.TLabelframe.Label", font=self.bold_font)
            labelframe_style = "Custom.TLabelframe"
        except Exception:
            labelframe_style = None
        # Set up custom style for all buttons
        style.configure("Custom.TButton", font=self.bold_font)

        # File info section
        if labelframe_style:
            info_frame = ttk.LabelFrame(main_frame, text="File Information", padding="10", style=labelframe_style)
        else:
            info_frame = ttk.LabelFrame(main_frame, text="File Information", padding="10")
        info_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        info_frame.columnconfigure(1, weight=1)
        
        ttk.Label(info_frame, text="Current Size:", font=self.regular_font).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.current_size_label = ttk.Label(info_frame, text="No file selected", font=self.regular_font)
        self.current_size_label.grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(info_frame, text="Estimated WebP Size:", font=self.regular_font).grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.estimated_size_label = ttk.Label(info_frame, text="No file selected", font=self.regular_font)
        self.estimated_size_label.grid(row=1, column=1, sticky=tk.W)
        
        # Output folder section
        ttk.Label(main_frame, text="Output Folder:", font=self.bold_font).grid(
            row=5, column=0, columnspan=3, sticky=tk.W, pady=(20, 5)
        )
        
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        output_frame.columnconfigure(0, weight=1)
        
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_folder, width=50, font=self.regular_font)
        self.output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(output_frame, text="Browse", command=self.browse_output, style="Custom.TButton").grid(
            row=0, column=1, sticky=tk.W
        )
        
        # Settings section
        if labelframe_style:
            settings_frame = ttk.LabelFrame(main_frame, text="Conversion Settings", padding="10", style=labelframe_style)
        else:
            settings_frame = ttk.LabelFrame(main_frame, text="Conversion Settings", padding="10")
        settings_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        settings_frame.columnconfigure(1, weight=1)
        
        # Quality slider
        ttk.Label(settings_frame, text="Quality:", font=self.regular_font).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        quality_frame = ttk.Frame(settings_frame)
        quality_frame.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        quality_frame.columnconfigure(0, weight=1)
        
        self.quality_scale = ttk.Scale(
            quality_frame, from_=1, to=100, orient=tk.HORIZONTAL, 
            variable=self.quality, command=self.update_quality_label
        )
        self.quality_scale.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.quality_label = ttk.Label(quality_frame, text="80%", font=self.regular_font)
        self.quality_label.grid(row=0, column=1, sticky=tk.W)
        
        # Max size slider
        ttk.Label(settings_frame, text="Max Size (longest side):", font=self.regular_font).grid(row=1, column=0, sticky=tk.W, pady=(10, 5))
        
        size_frame = ttk.Frame(settings_frame)
        size_frame.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 5))
        size_frame.columnconfigure(0, weight=1)
        
        self.size_scale = tk.Scale(
            size_frame, from_=100, to=4000, orient=tk.HORIZONTAL, 
            variable=self.max_size, command=self.update_size_label,
            resolution=100, showvalue=0
        )
        self.size_scale.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.size_label = ttk.Label(size_frame, text="1920px", font=self.regular_font)
        self.size_label.grid(row=0, column=1, sticky=tk.W)
        
        # Convert button
        self.convert_btn = ttk.Button(
            main_frame, text="Convert Selected Images", command=self.start_conversion,
            style="Custom.TButton"
        )
        self.convert_btn.grid(row=8, column=0, columnspan=3, pady=(20, 10))
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.grid(row=9, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready to convert images", font=self.regular_font)
        self.status_label.grid(row=10, column=0, columnspan=3, sticky=tk.W)
        
    def update_quality_label(self, value):
        self.quality_label.config(text=f"{int(float(value))}%")
        self.update_file_info()
        
    def update_size_label(self, value):
        self.size_label.config(text=f"{int(float(value))}px")
        self.update_file_info()
        
    def browse_files(self):
        filetypes = [
            ("Image files", "*.jpg *.jpeg *.JPG *.JPEG *.PNG *.png"),
            ("All files", "*.*")
        ]
        
        files = filedialog.askopenfilenames(
            title="Select JPG/JPEG images",
            filetypes=filetypes
        )
        
        if files:
            self.selected_files.extend(files)
            self.update_file_list()
            self.auto_update_max_size()
            self.auto_set_output_folder(files[0])  # Use first selected file's directory
            
    def auto_set_output_folder(self, first_file_path):
        """Automatically set output folder to the same directory as the input files"""
        try:
            input_directory = os.path.dirname(first_file_path)
            self.output_folder.set(input_directory)
        except Exception:
            pass  # If there's any error, just skip auto-setting
            
    def auto_update_max_size(self):
        """Automatically update the max size slider based on the largest image dimension"""
        if not self.selected_files:
            return
            
        max_dimension = 0
        
        for file_path in self.selected_files:
            try:
                with Image.open(file_path) as img:
                    width, height = img.size
                    largest_side = max(width, height)
                    max_dimension = max(max_dimension, largest_side)
            except Exception:
                continue  # Skip files that can't be opened
                
        if max_dimension > 0:
            # Round up to nearest 100
            suggested_size = ((max_dimension + 99) // 100) * 100
            # Ensure it's within our slider range
            suggested_size = max(100, min(4000, suggested_size))
            self.max_size.set(suggested_size)
            self.update_size_label(suggested_size)
            
    def clear_files(self):
        self.selected_files.clear()
        self.update_file_list()
        
    def update_file_list(self):
        self.file_listbox.delete(0, tk.END)
        for file in self.selected_files:
            filename = os.path.basename(file)
            self.file_listbox.insert(tk.END, filename)
            
    def browse_output(self):
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.output_folder.set(folder)
            
    def resize_image(self, img, max_size, preserve_aspect):
        if not preserve_aspect:
            return img.resize((max_size, max_size), Image.LANCZOS)
            
        # Calculate new size while preserving aspect ratio
        width, height = img.size
        if width > height:
            new_width = max_size
            new_height = int((height * max_size) / width)
        else:
            new_height = max_size
            new_width = int((width * max_size) / height)
            
        return img.resize((new_width, new_height), Image.LANCZOS)
    
    def format_file_size(self, size_bytes):
        """Convert bytes to human readable format"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
    
    def on_file_select(self, event):
        """Handle file selection in listbox"""
        self.update_file_info()
    
    def estimate_webp_factor(self, quality):
        # Piecewise linear interpolation based on your measurements
        if quality >= 95:
            return 0.429
        elif quality >= 80:
            # Between 90 (0.124) and 100 (0.429)
            return 0.124 + (quality - 90) * (0.429 - 0.124) / 10
        elif quality >= 60:
            # Between 70 (0.062) and 90 (0.124)
            return 0.062 + (quality - 70) * (0.124 - 0.062) / 20
        elif quality >= 50:
            # Between 50 (0.050) and 70 (0.062)
            return 0.050 + (quality - 50) * (0.062 - 0.050) / 20
        else:
            # Below 50, assume 0.050
            return 0.050

    def update_file_info(self):
        """Update file size information for selected file"""
        selection = self.file_listbox.curselection()
        if not selection or not self.selected_files:
            self.current_size_label.config(text="No file selected")
            self.estimated_size_label.config(text="No file selected")
            return

        try:
            selected_index = selection[0]
            if selected_index >= len(self.selected_files):
                return

            file_path = self.selected_files[selected_index]
            current_size = os.path.getsize(file_path)
            self.current_size_label.config(text=self.format_file_size(current_size))

            with Image.open(file_path) as img:
                width, height = img.size
                original_pixels = width * height

                max_size = self.max_size.get()
                if width > height:
                    new_width = min(max_size, width)
                    new_height = int((height * new_width) / width)
                else:
                    new_height = min(max_size, height)
                    new_width = int((width * new_height) / height)

                new_pixels = new_width * new_height
                pixel_ratio = new_pixels / original_pixels

                quality = self.quality.get()
                # Use interpolation between your measured points
                if quality >= 95:
                    webp_factor = 0.45
                elif quality >= 85:
                    webp_factor = 0.13
                elif quality >= 60:
                    webp_factor = 0.065
                elif quality >= 40:
                    webp_factor = 0.053
                else:
                    webp_factor = 0.04

                estimated_size = current_size * pixel_ratio * webp_factor
                self.estimated_size_label.config(text=self.format_file_size(int(estimated_size)))

        except Exception as e:
            self.current_size_label.config(text="Error reading file")
            self.estimated_size_label.config(text="Cannot estimate")
        
    def convert_images(self):
        # Get selected files from listbox
        selection = self.file_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select at least one image file from the list.")
            return
            
        # Get the actual file paths for selected indices
        files_to_convert = []
        for index in selection:
            if index < len(self.selected_files):
                files_to_convert.append(self.selected_files[index])
        
        if not files_to_convert:
            messagebox.showerror("Error", "No valid files selected for conversion.")
            return
            
        output_dir = self.output_folder.get()
        if not output_dir:
            messagebox.showerror("Error", "Please select an output folder.")
            return
            
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        total_files = len(files_to_convert)
        converted_count = 0
        failed_files = []
        
        self.progress['maximum'] = total_files
        self.progress['value'] = 0
        
        for i, file_path in enumerate(files_to_convert):
            try:
                # Update status
                filename = os.path.basename(file_path)
                self.status_label.config(text=f"Converting: {filename}")
                self.root.update()
                
                # Open and process image
                with Image.open(file_path) as img:
                    # Convert to RGB if necessary
                    if img.mode in ('RGBA', 'LA', 'P'):
                        img = img.convert('RGB')
                    
                    # Resize image (always preserve aspect ratio)
                    img_resized = self.resize_image(img, self.max_size.get(), self.preserve_aspect)
                    
                    # Generate output filename
                    input_name = Path(file_path).stem
                    output_path = os.path.join(output_dir, f"{input_name}.webp")
                    
                    # Save as WebP
                    img_resized.save(
                        output_path, 
                        'WebP', 
                        quality=self.quality.get(),
                        optimize=True
                    )
                    
                converted_count += 1
                
            except Exception as e:
                failed_files.append(f"{filename}: {str(e)}")
                
            # Update progress
            self.progress['value'] = i + 1
            self.root.update()
            
        # Show completion message
        if failed_files:
            error_msg = f"Conversion completed with errors.\n\nConverted: {converted_count}/{total_files}\n\nFailed files:\n" + "\n".join(failed_files[:5])
            if len(failed_files) > 5:
                error_msg += f"\n... and {len(failed_files) - 5} more"
            messagebox.showwarning("Conversion Complete", error_msg)
        else:
            messagebox.showinfo("Success", f"Successfully converted {converted_count} images to WebP format!")
            
        self.status_label.config(text="Conversion completed")
        self.convert_btn.config(state=tk.NORMAL)
        
    def start_conversion(self):
        self.convert_btn.config(state=tk.DISABLED)
        # Run conversion in a separate thread to prevent UI freezing
        thread = threading.Thread(target=self.convert_images)
        thread.daemon = True
        thread.start()

    def preview_selected_image(self):
        selection = self.file_listbox.curselection()
        if not selection or not self.selected_files:
            messagebox.showinfo("Preview", "Please select a file to preview.")
            return
        index = selection[0]
        if index >= len(self.selected_files):
            messagebox.showinfo("Preview", "Invalid selection.")
            return
        file_path = self.selected_files[index]
        try:
            with Image.open(file_path) as img:
                # Resize for preview if too large
                max_preview_size = 800
                width, height = img.size
                if max(width, height) > max_preview_size:
                    if width > height:
                        new_width = max_preview_size
                        new_height = int((height * new_width) / width)
                    else:
                        new_height = max_preview_size
                        new_width = int((width * new_height) / height)
                    img = img.resize((new_width, new_height), Image.LANCZOS)
                # Convert to PhotoImage
                img_tk = None
                try:
                    from PIL import ImageTk
                    img_tk = ImageTk.PhotoImage(img)
                except ImportError:
                    messagebox.showerror("Preview Error", "Pillow's ImageTk is required for preview.")
                    return
                # Create preview window
                preview_win = tk.Toplevel(self.root)
                preview_win.title(f"Preview: {os.path.basename(file_path)}")
                preview_win.resizable(True, True)
                label = ttk.Label(preview_win, image=img_tk)
                label.image = img_tk  # Keep reference
                label.pack(padx=10, pady=10)
        except Exception as e:
            messagebox.showerror("Preview Error", f"Could not open image:\n{e}")

def main():
    root = tk.Tk()
    app = ImageConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()