import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import os

from compression_manager import compression
from PIL import Image, ImageTk

from custom_exceptions import InvalidBlockSizeError, InvalidFrequenciesNumberError



class GUI:
    """GUI for image compression."""

    COLORS = {
        'primary_bg': '#68ba7f',
        'secondary_bg': '#377E4B',
        'text_primary': '#253d2c',
        'error': '#BF1029',
        'light_bg': '#f0f0ed',
        'lightgray': 'lightgray'
    }

    FONTS = {
        'title': ('Mansfield', 25),
        'subtitle': ('Mansfield', 16),
        'error': ('TimesNewRoman', 16)
    }

    def __init__(self):
        self.root = tk.Tk()
        self.selected_file = None
        self.setup_interface()
        self.max_size = (700, 700)

    def setup_interface(self):
        self.root.title('Image compressor')
        self.root.resizable(True, True)
        self.root.configure(bg=self.COLORS['primary_bg'])

        # Set the window size to 75% of the scre
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = int(screen_width * 0.75)
        window_height = int(screen_height * 0.75)
        self.root.geometry(f"{window_width}x{window_height}")

        # Style definition
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("BG.TFrame", 
                       foreground=self.COLORS['text_primary'], 
                       background=self.COLORS['primary_bg'])
        
        style.configure("BG_LABEL.TLabel", 
                       foreground=self.COLORS['text_primary'], 
                       background=self.COLORS['primary_bg'])
        
        style.configure("BG_IMAGE.TFrame", 
                       foreground=self.COLORS['text_primary'], 
                       background=self.COLORS['secondary_bg'])
        
        style.configure("BG_IMAGE.TLabel", 
                       foreground=self.COLORS['text_primary'], 
                       background=self.COLORS['secondary_bg'])


        # Set up the interface elements

        main_frame = ttk.Frame(self.root, padding="30", style="BG.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=(250, 250))

        # TITLE SECTION
        title_label = ttk.Label(
            main_frame,
            text="Image Compressor",
            style="BG_LABEL.TLabel",
            font= self.FONTS["title"]
        )
        title_label.pack(pady=(0, 30))


        # FILE SECTION
        self.file_frame = ttk.Frame(main_frame, style = "BG.TFrame")
        self.file_frame.pack(fill=tk.X, pady=(0, 20))
        
        file_label = ttk.Label(
            self.file_frame, 
            text="Select a Bitmap Image:",
            style="BG_LABEL.TLabel",
            font = self.FONTS["subtitle"]
        )
        file_label.pack(anchor=tk.W, pady=(0, 10))
        
        file_button_frame = tk.Frame(self.file_frame)
        file_button_frame.pack(fill=tk.X)
            
        open_button = ttk.Button(
            file_button_frame,
            text='Choose File',
            command=self.select_file
        )
        open_button.pack(side=tk.LEFT)
        
        self.file_path_label = ttk.Label(
            file_button_frame,
            text="No file selected",
            background=self.COLORS["light_bg"]
        )
        self.file_path_label.pack(side=tk.LEFT, padx=(15, 0), fill=tk.X, expand=True)


        # PARAMETERS SECTION
        parameters_frame = ttk.Frame(main_frame, style="BG.TFrame")
        parameters_frame.pack(fill=tk.X, pady=(20, 0))
        parameters_title = ttk.Label(
                parameters_frame,
                text="Compression Parameters:",
                style="BG_LABEL.TLabel",
                font=self.FONTS["subtitle"]
            )
        parameters_title.pack(anchor=tk.W, pady=(0, 15))

        # F parameter
        f_frame = tk.Frame(parameters_frame)
        f_frame.pack(fill=tk.X, pady=(0, 15))
            
        f_label = tk.Label(
            f_frame,
            text="Block Size (F):",
            width=20,
            anchor='w'
        )
        f_label.pack(side=tk.LEFT)

        self.f_entry = tk.Entry(
            f_frame,
            width=15
        )
        self.f_entry.pack(side=tk.LEFT, padx=(10, 0))

        f_desc = tk.Label(
            f_frame,
            text="(Integer value for block width)"
        )
        f_desc.pack(side=tk.LEFT, padx=(10, 0))
            
        # d parameter
        d_frame = tk.Frame(parameters_frame)
        d_frame.pack(fill=tk.X, pady=(0, 15))
        
        d_label = tk.Label(
            d_frame,
            text="Frequency Threshold (d):",
            width=20
        )
        d_label.pack(side=tk.LEFT)
        
        self.d_entry = tk.Entry(
            d_frame,
            width=15
        )
        self.d_entry.pack(side=tk.LEFT, padx=(10, 0))
            
        d_desc = tk.Label(
            d_frame,
            text="(Integer: 0 ≤ d ≤ 2F-2)"
        )
        d_desc.pack(side=tk.LEFT, padx=(10, 0))
        
        # Button section
        button_frame = ttk.Frame(main_frame, style="BG.TFrame")
        button_frame.pack(pady=(30, 0))
        
        start_button = ttk.Button(
            button_frame,
            text='Start Compression',
            command=self.start_compression,
        )
        start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_button = ttk.Button(
            button_frame,
            text='Clear All',
            command=self.clear_all
        )
        clear_button.pack(side=tk.LEFT)
        
        # IMAGES SECTION

        images_frame = ttk.Frame(main_frame, style="BG.TFrame")
        images_frame.pack(fill=tk.X, pady=(20, 0))
        images_title = ttk.Label(
                images_frame,
                text="Image comparison:",
                anchor="center",
                style="BG_LABEL.TLabel",
                font=self.FONTS["subtitle"]
            )
        images_title.pack(pady=(0, 15))

        # On the left the original image, on the right the compressed one

        frame_image_original = ttk.Frame(images_frame, style="BG_IMAGE.TFrame")
        frame_image_original.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)
        
        self.label_original_image = ttk.Label(frame_image_original, anchor="center", style="BG_IMAGE.TLabel")
        self.label_original_image.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.label_original = ttk.Label(
            frame_image_original, 
            text="Original image", 
            anchor="center", 
            background=self.COLORS["lightgray"],
            font=self.FONTS["subtitle"]
            )
        self.label_original.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        frame_image_compressed = ttk.Frame(images_frame, style="BG_IMAGE.TFrame")
        frame_image_compressed.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)
        
        self.label_compressed_image = ttk.Label(frame_image_compressed, anchor="center", style="BG_IMAGE.TLabel")
        self.label_compressed_image.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.label_compressed = ttk.Label(
            frame_image_compressed,
            text="Compressed image",
            anchor="center",
            background=self.COLORS["lightgray"],
            font=self.FONTS["subtitle"]
            )
        self.label_compressed.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        #Error section
        
        self.label_errors = ttk.Label(
            main_frame,
            anchor="center",
            foreground=self.COLORS['text_primary'],
            style="BG_LABEL.TLabel",
            font=self.FONTS["error"]
        )
        self.label_errors.pack(fill=tk.X, padx=20, pady=5)


    def start_compression(self):
        """Validate compression parameters and compress the image."""
        f_value = self.f_entry.get().strip()
        d_value = self.d_entry.get().strip()

        try:
            f = int(f_value)
            d = int(d_value)
            
            self.label_errors.config(text = f"Starting compression with F={f}, d={d}, file={self.selected_file} ...", foreground=self.COLORS['text_primary'])            
            self.label_errors.update()
            
            # Validate the F and d values
            if d < 0 or d > 2*f-2:
                self.label_errors.config(text=f"Invalid d value. Must be between 0 and {2*f-2}.", foreground=self.COLORS['error'])
                return
                
            output_path = compression(self.selected_file, f, d)

            # Check if the image exists and load it 
            if self.selected_file:
                original_image = Image.open(self.selected_file)
                compressed_image = Image.open(output_path)

                original_image.thumbnail(self.max_size)
                compressed_image.thumbnail(self.max_size)

            else:
                self.label_errors.config(text="A problem occurred while loading the inserted file, please retry or change", foreground=self.COLORS['error'])

            # Convert the images in a tkinter format
            self.original_photo_tk = ImageTk.PhotoImage(original_image)
            self.compressed_photo_tk = ImageTk.PhotoImage(compressed_image)
            
            # Load the images in the GUI
            self.label_original_image.configure(image=self.original_photo_tk)
            self.label_compressed_image.configure(image=self.compressed_photo_tk)    
            
            self.label_errors.config(text = "The Image has been compressed !", foreground=self.COLORS['text_primary'])

        except InvalidBlockSizeError as e:
            self.label_errors.config(text=e.msg, foreground=self.COLORS['error'])
        
        except InvalidFrequenciesNumberError as e:
            self.label_errors.config(text=e.msg, foreground=self.COLORS['error'])

        except ValueError:
            self.label_errors.config(text="Invalid values. F and d must be integers.", foreground=self.COLORS['error'])


    def select_file(self):
        """Handle file selection."""
        filetypes = [('Gray scale images', '*.bmp')]
        
        filename = fd.askopenfilename(
            title='Open a bitmap image',
            initialdir='/',
            filetypes=filetypes
        )

        if filename:
            self.selected_file = filename
            # Display only the filename, not the full path
            display_name = os.path.basename(filename)
            self.file_path_label.configure(text=display_name)
            print(f"Selected file: {filename}")


    def clear_all(self):
        """Clear all inputs, selections, and displayed content."""
        
        # Clear file selection
        self.selected_file = None
        self.file_path_label.configure(text="No file selected")
        
        # Clear parameter entries
        self.f_entry.delete(0, tk.END)
        self.d_entry.delete(0, tk.END)
        
        #Clear error/status messages
        self.label_errors.config(text="")
        
        # Clear images
        self.label_original_image.configure(image="")
        self.label_compressed_image.configure(image="")
            
        # Clear image references to free memory
        if hasattr(self, 'original_photo_tk'):
            del self.original_photo_tk
        if hasattr(self, 'compressed_photo_tk'):
            del self.compressed_photo_tk         

    def run(self):
        """Start the GUI main loop."""
        self.root.mainloop()

def load_gui():
    """Create and run the GUI application."""
    app = GUI()
    app.run()

if __name__ == "__main__":
    load_gui()