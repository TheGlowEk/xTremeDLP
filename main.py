import sys
import os
import subprocess
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class YTDLPGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("xTremeDLP")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        self.root.overrideredirect(True)
        self.root.iconbitmap("./icon.ico")

        self.center_window()

        self.style = ttk.Style()
        self.style.theme_use('default')

        self.dark_bg = '#1b1b1b'
        self.darker_bg = '#1e1e1e'
        self.accent = '#111111'
        self.text = '#ffffff'
        self.highlight = '#330000'
        self.selection_bg = '#214283'

        self.title_bar = ttk.Frame(self.root, style='Title.TFrame')
        self.title_bar.pack(fill='x')

        self.title_label = ttk.Label(self.title_bar, text="xTremeDLP", style='Title.TLabel')
        self.title_label.pack(side='left', padx=10)

        self.close_button = ttk.Button(self.title_bar, text='×', width=3, command=self.root.destroy)
        self.close_button.pack(side='right')

        self.minimize_button = ttk.Button(self.title_bar, text='−', width=3, command=self.minimize_window)
        self.minimize_button.pack(side='right')

        self.title_bar.bind('<Button-1>', self.start_move)
        self.title_bar.bind('<B1-Motion>', self.do_move)
        self.title_bar.bind('<ButtonRelease-1>', self.stop_move)
        self.title_label.bind('<Button-1>', self.start_move)
        self.title_label.bind('<B1-Motion>', self.do_move)
        self.title_label.bind('<ButtonRelease-1>', self.stop_move)

        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill='both', expand=True)

        self.root.configure(bg=self.dark_bg)
        self.style.configure('TFrame', background=self.dark_bg)
        self.style.configure('TLabel', background=self.dark_bg, foreground=self.text)
        self.style.configure('TButton', background=self.accent, foreground=self.text, padding=5, relief='flat')
        self.style.map('TButton', background=[('active', self.highlight)])

        self.style.configure('TEntry', fieldbackground=self.darker_bg, foreground=self.text, padding=5)

        self.style.configure('Treeview', background=self.darker_bg, foreground=self.text, fieldbackground=self.darker_bg)
        self.style.configure('Treeview.Heading', background=self.accent, foreground=self.text, relief='flat')
        self.style.map('Treeview', background=[('selected', self.selection_bg)], foreground=[('selected', self.text)])
        self.style.map('Treeview.Heading', background=[('active', self.highlight)])

        self.style.configure('Vertical.TScrollbar', background=self.accent, arrowcolor=self.text, bordercolor=self.accent, troughcolor=self.darker_bg)
        self.style.configure('Horizontal.TScrollbar', background=self.accent, arrowcolor=self.text, bordercolor=self.accent, troughcolor=self.darker_bg)

        self.style.configure('Title.TFrame', background=self.dark_bg)
        self.style.configure('Title.TLabel', background=self.dark_bg, foreground=self.text, font=('Arial', 10))
        self.style.configure('Title.TButton', background=self.dark_bg, foreground=self.text, font=('Arial', 13, 'bold'), borderwidth=0)
        self.style.map('Title.TButton', background=[('active', self.highlight)], foreground=[('active', self.text)])

        self.title_bar.configure(style='Title.TFrame')
        self.title_label.configure(style='Title.TLabel')
        self.close_button.configure(style='Title.TButton')
        self.minimize_button.configure(style='Title.TButton')

        self.yt_dlp_path = "yt-dlp.exe"
        self.ffmpeg_path = "ffmpeg.exe"

        if not os.path.exists(self.yt_dlp_path):
            if os.path.exists("./yt-dlp.exe"):
                self.yt_dlp_path = "./yt-dlp.exe"
            else:
                messagebox.showerror("Error", "yt-dlp.exe not found. Make sure the program is in the same directory as the application.")
                root.destroy()
                return

        if not os.path.exists(self.ffmpeg_path):
            if os.path.exists("./ffmpeg.exe"):
                self.ffmpeg_path = "./ffmpeg.exe"
            else:
                messagebox.showerror("Error", "ffmpeg.exe not found. Some features may be unavailable.")

        self.download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        self.create_widgets()

    def center_window(self):
        width = 800
        height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def minimize_window(self):
        self.root.withdraw()
        self.root.overrideredirect(False)
        self.root.iconify()

    def deiconify_window(self, event=None):
        self.root.overrideredirect(True)
        self.root.deiconify()

    def start_move(self, event):
        self.x = event.x_root - self.root.winfo_x()
        self.y = event.y_root - self.root.winfo_y()
        self.root.attributes('-alpha', 0.5)

    def do_move(self, event):
        x = event.x_root - self.x
        y = event.y_root - self.y
        self.root.geometry(f'+{x}+{y}')

    def stop_move(self, event):
        self.root.attributes('-alpha', 1.0)

    def create_widgets(self):
        main_frame = ttk.Frame(self.main_container, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(url_frame, text="URL:").pack(side=tk.LEFT, padx=(0, 5))
        self.url_entry = ttk.Entry(url_frame)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(url_frame, text="Get Info", command=self.fetch_formats).pack(side=tk.LEFT)

        folder_frame = ttk.Frame(main_frame)
        folder_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(folder_frame, text="Target folder:").pack(side=tk.LEFT, padx=(0, 5))
        self.folder_entry = ttk.Entry(folder_frame)
        self.folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.folder_entry.insert(0, self.download_folder)
        ttk.Button(folder_frame, text="Browse", command=self.select_folder).pack(side=tk.LEFT)

        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        ttk.Label(list_frame, text="Available formats:").pack(anchor=tk.W)

        formats_frame = ttk.Frame(list_frame)
        formats_frame.pack(fill=tk.BOTH, expand=True)

        columns = (
            "format_id", "extension", "resolution", "fps", "vcodec", "acodec", "vbitrate", "abitrate", "filesize")
        self.formats_tree = ttk.Treeview(formats_frame, columns=columns, show="headings", selectmode="browse")

        self.formats_tree.heading("format_id", text="ID", command=lambda: self.treeview_sort_column("format_id", False))
        self.formats_tree.heading("extension", text="Format", command=lambda: self.treeview_sort_column("extension", False))
        self.formats_tree.heading("resolution", text="Resolution", command=lambda: self.treeview_sort_column("resolution", False))
        self.formats_tree.heading("fps", text="FPS", command=lambda: self.treeview_sort_column("fps", False))
        self.formats_tree.heading("vcodec", text="Video Codec", command=lambda: self.treeview_sort_column("vcodec", False))
        self.formats_tree.heading("acodec", text="Audio Codec", command=lambda: self.treeview_sort_column("acodec", False))
        self.formats_tree.heading("vbitrate", text="Video kb/s", command=lambda: self.treeview_sort_column("vbitrate", False))
        self.formats_tree.heading("abitrate", text="Audio kb/s", command=lambda: self.treeview_sort_column("abitrate", False))
        self.formats_tree.heading("filesize", text="Size", command=lambda: self.treeview_sort_column("filesize", False))

        self.formats_tree.column("format_id", width=60, minwidth=50)
        self.formats_tree.column("extension", width=60, minwidth=50)
        self.formats_tree.column("resolution", width=100, minwidth=80)
        self.formats_tree.column("fps", width=50, minwidth=40)
        self.formats_tree.column("vcodec", width=100, minwidth=80)
        self.formats_tree.column("acodec", width=100, minwidth=80)
        self.formats_tree.column("vbitrate", width=80, minwidth=70)
        self.formats_tree.column("abitrate", width=80, minwidth=70)
        self.formats_tree.column("filesize", width=80, minwidth=60)

        vsb = ttk.Scrollbar(formats_frame, orient=tk.VERTICAL, command=self.formats_tree.yview)
        hsb = ttk.Scrollbar(formats_frame, orient=tk.HORIZONTAL, command=self.formats_tree.xview)
        self.formats_tree.configure(yscroll=vsb.set, xscroll=hsb.set)

        self.formats_tree.bind("<ButtonRelease-1>", self.on_item_click)

        self.formats_tree.grid(column=0, row=0, sticky='nsew')
        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew')

        formats_frame.columnconfigure(0, weight=1)
        formats_frame.rowconfigure(0, weight=1)

        select_frame = ttk.Frame(main_frame)
        select_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(select_frame, text="Select All", command=self.select_all).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(select_frame, text="Deselect All", command=self.deselect_all).pack(side=tk.LEFT)

        download_frame = ttk.Frame(main_frame)
        download_frame.pack(fill=tk.X)

        self.download_button = ttk.Button(download_frame, text="Download Selected", command=self.download_selected)
        self.download_button.pack(fill=tk.X)
        self.download_button["state"] = "disabled"

        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(10, 0))

        self.style.configure("Red.Horizontal.TProgressbar", troughcolor=self.darker_bg, bordercolor=self.accent, background="red", lightcolor="red", darkcolor="darkred")

        self.progress_bar = ttk.Progressbar(status_frame, mode='indeterminate', style='Red.Horizontal.TProgressbar')
        self.progress_bar.pack(fill=tk.X)

        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var, anchor=tk.W)
        self.status_label.pack(fill=tk.X)

        self.formats_data = []

    def treeview_sort_column(self, col, reverse):
        data = [(self.formats_tree.set(k, col), k) for k in self.formats_tree.get_children('')]

        try:
            if col == "resolution":
                numeric_data = []
                for item, k in data:
                    if "x" in item and item != "N/A":
                        width, height = map(int, item.split("x"))
                        pixel_count = width * height
                        numeric_data.append((pixel_count, k))
                    else:
                        numeric_data.append((0, k))
                data = numeric_data
            elif col == "filesize":
                numeric_data = []
                for item, k in data:
                    try:
                        if "MB" in item:
                            size = float(item.replace("MB", "").strip().replace("~", ""))
                            numeric_data.append((size, k))
                        elif "GB" in item:
                            size = float(item.replace("GB", "").strip().replace("~", "")) * 1024
                            numeric_data.append((size, k))
                        elif "KB" in item:
                            size = float(item.replace("KB", "").strip().replace("~", "")) / 1024
                            numeric_data.append((size, k))
                        elif "B" in item:
                            size = float(item.replace("B", "").strip().replace("~", "")) / (1024 * 1024)
                            numeric_data.append((size, k))
                        else:
                            numeric_data.append((0, k))
                    except:
                        numeric_data.append((0, k))
                data = numeric_data
            elif col in ["fps", "vbitrate", "abitrate"]:
                numeric_data = []
                for item, k in data:
                    try:
                        if item != "N/A":
                            cleaned_item = ''.join(c for c in item if c.isdigit() or c == '.')
                            value = float(cleaned_item) if cleaned_item else 0
                            numeric_data.append((value, k))
                        else:
                            numeric_data.append((0, k))
                    except:
                        numeric_data.append((0, k))
                data = numeric_data
            elif col == "format_id":
                str_data = []
                for item, k in data:
                    str_data.append((item, k))
                data = str_data
        except:
            pass

        try:
            data.sort(key=lambda x: x[0] if isinstance(x[0], (int, float)) else str(x[0]).lower(), reverse=reverse)
        except:
            data.sort(key=lambda x: str(x[0]).lower(), reverse=reverse)

        for indx, (val, k) in enumerate(data):
            self.formats_tree.move(k, '', indx)

        self.formats_tree.heading(col, command=lambda: self.treeview_sort_column(col, not reverse))

        for i, format_data in enumerate(self.formats_data):
            item_id = format_data["id"]
            if format_data["selected"]:
                self.formats_tree.item(item_id, tags=('selected',))

    def on_item_click(self, event):
        region = self.formats_tree.identify("region", event.x, event.y)
        if region == "heading":
            return

        item_id = self.formats_tree.identify('item', event.x, event.y)
        if item_id:
            for i, format_info in enumerate(self.formats_data):
                if format_info["id"] == item_id:
                    self.formats_data[i]["selected"] = not self.formats_data[i]["selected"]
                    self.update_item_display(item_id, self.formats_data[i]["selected"])
                    break

    def update_item_display(self, item_id, selected):
        if selected:
            self.formats_tree.item(item_id, tags=('selected',))
        else:
            self.formats_tree.item(item_id, tags=())

        self.formats_tree.tag_configure('selected', background=self.selection_bg)

    def select_folder(self):
        folder = filedialog.askdirectory(initialdir=self.download_folder)
        if folder:
            self.download_folder = folder
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder)

    def fetch_formats(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a valid URL")
            return

        self.status_var.set("Getting format information...")
        self.progress_bar.start(10)
        self.root.update()

        for item in self.formats_tree.get_children():
            self.formats_tree.delete(item)

        self.formats_data = []

        self.formats_tree.tag_configure('selected', background='#CCE5FF')

        try:
            cmd_best_audio = [self.yt_dlp_path, "-f", "bestaudio", "-J", "--no-check-certificates", url]
            result_best_audio = subprocess.run(cmd_best_audio, capture_output=True, text=True)
            best_audio_data = json.loads(result_best_audio.stdout)
            best_audio_codec = best_audio_data.get("acodec", "")

            best_audio_bitrate = ""
            if best_audio_data.get("abr"):
                best_audio_bitrate = f"{int(best_audio_data['abr'])}"
            elif best_audio_data.get("tbr") and best_audio_data.get("vcodec") == "none":
                best_audio_bitrate = f"{int(best_audio_data['tbr'])}"

            acodec_mapping = {
                'mp4a': 'AAC',
                'mp3': 'MP3',
                'opus': 'Opus',
                'vorbis': 'Vorbis',
                'aac': 'AAC',
                'm4a': 'AAC',
                'ac3': 'AC3',
                'eac3': 'EAC3',
                'dtse': 'DTS',
                'dts': 'DTS',
                'flac': 'FLAC',
                'alac': 'ALAC',
                'wav': 'WAV',
                'pcm': 'PCM'
            }

            if best_audio_codec.startswith('opus'):
                best_audio_name = 'Opus'
            elif best_audio_codec.startswith('mp4a'):
                best_audio_name = 'AAC'
            else:
                base_acodec = best_audio_codec.split('.')[0].lower()
                best_audio_name = acodec_mapping.get(base_acodec, base_acodec.upper())

            cmd = [self.yt_dlp_path, "-J", "--no-check-certificates", url]
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                self.progress_bar.stop()
                messagebox.showerror("Error", f"Error getting information: {result.stderr}")
                self.status_var.set("Error")
                return

            data = json.loads(result.stdout)

            for format_info in data.get("formats", []):
                format_id = format_info.get("format_id", "")
                extension = format_info.get("ext", "")
                vcodec = format_info.get("vcodec", "")
                acodec = format_info.get("acodec", "")

                if vcodec == "none" and extension == "webm":
                    vcodec = ""
                    resolution = ""
                    fps = ""
                    vbitrate = ""
                    acodec = "Opus"
                    extension = "opus"
                else:
                    resolution = ""
                    if format_info.get("width") and format_info.get("height"):
                        resolution = f"{format_info.get('width')}x{format_info.get('height')}"

                    fps = format_info.get("fps", "")
                    if fps and fps is not None:
                        try:
                            fps = str(int(float(fps)))
                        except (ValueError, TypeError):
                            fps = ""

                    vbitrate = ""
                    if vcodec == "none":
                        vcodec = ""
                        vbitrate = ""
                    else:
                        vcodec_mapping = {
                            'avc1': 'H.264',
                            'vp9': 'VP9',
                            'av01': 'AV1',
                            'vp8': 'VP8'
                        }
                        base_codec = vcodec.split('.')[0].lower()
                        vcodec = vcodec_mapping.get(base_codec, base_codec.upper())

                        if format_info.get("vbr"):
                            vbitrate = f"{int(format_info['vbr'])}"
                        elif format_info.get("tbr"):
                            vbitrate = f"~{int(format_info['tbr'])}"

                abitrate = ""
                if acodec == "none":
                    acodec = ""
                    abitrate = ""
                    if "youtube.com" in url and vcodec:
                        acodec = best_audio_name
                        abitrate = best_audio_bitrate
                else:
                    if acodec.startswith('opus'):
                        acodec = 'Opus'
                    elif acodec.startswith('mp4a'):
                        acodec = 'AAC'
                    else:
                        base_acodec = acodec.split('.')[0].lower()
                        acodec = acodec_mapping.get(base_acodec, base_acodec.upper())

                    if format_info.get("abr"):
                        abitrate = f"{int(format_info['abr'])}"
                    elif format_info.get("tbr") and not vcodec:
                        abitrate = f"~{int(format_info['tbr'])}"

                filesize = "N/A"
                if format_info.get("filesize"):
                    size_bytes = format_info["filesize"]
                    if size_bytes < 1024:
                        filesize = f"{size_bytes} B"
                    elif size_bytes < 1024 * 1024:
                        filesize = f"{size_bytes / 1024:.1f} KB"
                    elif size_bytes < 1024 * 1024 * 1024:
                        filesize = f"{size_bytes / (1024 * 1024):.1f} MB"
                    else:
                        filesize = f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"
                elif format_info.get("filesize_approx"):
                    size_bytes = format_info["filesize_approx"]
                    filesize = f"~{size_bytes / (1024 * 1024):.1f} MB"

                values = (format_id, extension, resolution, fps, vcodec, acodec, vbitrate, abitrate, filesize)
                item_id = self.formats_tree.insert("", "end", values=values, tags=(''))

                self.formats_data.append({
                    "id": item_id,
                    "format_id": format_id,
                    "selected": False
                })

            self.progress_bar.stop()
            self.download_button["state"] = "normal"
            self.status_var.set(f"Found {len(self.formats_data)} formats")

        except Exception as e:
            self.progress_bar.stop()
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_var.set("Error")

    def select_all(self):
        for i, format_data in enumerate(self.formats_data):
            self.formats_data[i]["selected"] = True
            self.update_item_display(format_data["id"], True)

    def deselect_all(self):
        for i, format_data in enumerate(self.formats_data):
            self.formats_data[i]["selected"] = False
            self.update_item_display(format_data["id"], False)

    def download_selected(self):
        selected_formats = [f["format_id"] for f in self.formats_data if f["selected"]]

        if not selected_formats:
            messagebox.showerror("Error", "No format selected")
            return

        url = self.url_entry.get().strip()
        output_dir = self.folder_entry.get()

        if not os.path.isdir(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                messagebox.showerror("Error", f"Cannot create target directory: {str(e)}")
                return

        try:
            cmd_info = [self.yt_dlp_path, "-J", "--no-check-certificates", url]
            result = subprocess.run(cmd_info, capture_output=True, text=True)

            if result.returncode != 0:
                messagebox.showerror("Error", f"Error getting information: {result.stderr}")
                return

            data = json.loads(result.stdout)
            format_extensions = {}

            for format_info in data.get("formats", []):
                format_id = format_info.get("format_id", "")
                extension = format_info.get("ext", "")
                format_extensions[format_id] = extension

        except Exception as e:
            messagebox.showerror("Error", f"Error analyzing formats: {str(e)}")
            return

        for format_id in selected_formats:
            self.status_var.set(f"Downloading format {format_id}...")
            self.progress_bar.start(10)
            self.root.update()

            try:
                output_template = os.path.join(output_dir, "%(title)s-%(format_id)s.%(ext)s")
                format_spec = f"{format_id}+bestaudio/bestaudio[ext=m4a]/bestaudio"

                cmd = [
                    self.yt_dlp_path,
                    "-f", format_spec,
                    "--ffmpeg-location", self.ffmpeg_path,
                    "--no-check-certificate",
                    "-o", output_template,
                    url
                ]

                if format_id in format_extensions and format_extensions[format_id] == "mp4":
                    cmd.insert(3, "--merge-output-format")
                    cmd.insert(4, "mp4")

                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)

                for line in iter(process.stdout.readline, ""):
                    self.status_var.set(line.strip())
                    self.root.update()

                process.stdout.close()
                return_code = process.wait()

                if return_code != 0:
                    self.progress_bar.stop()
                    error = process.stderr.read()
                    messagebox.showerror("Error", f"Error downloading format {format_id}: {error}")

            except Exception as e:
                self.progress_bar.stop()
                messagebox.showerror("Error", f"An error occurred during download: {str(e)}")

        self.progress_bar.stop()
        self.status_var.set("Download complete")
        messagebox.showinfo("Success", "Download completed")

if __name__ == "__main__":
    root = tk.Tk()
    app = YTDLPGUI(root)
    root.mainloop()