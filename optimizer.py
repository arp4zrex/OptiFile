import os
import mimetypes
from PIL import Image
import ffmpeg
import PyPDF2
import gzip
import shutil
from pydub import AudioSegment
from pydub.utils import which
import threading

AudioSegment.converter = which("ffmpeg")
AudioSegment.ffprobe = which("ffprobe")

def update_progress_bar(progress_bar, file_label, progress):
    progress_bar['value'] = progress
    file_label.config(text=f"Optimizing... {progress}%")
    if progress >= 100:
        messagebox.showinfo("Success", "File optimized successfully")

def optimize_image(input_path, output_path):
    with Image.open(input_path) as img:
        img.save(output_path, optimize=True, quality=70)

def optimize_video(input_path, output_path):
    (
        ffmpeg
        .input(input_path)
        .output(output_path, vcodec='libx264', crf=23, preset='medium')
        .run()
    )

def optimize_pdf(input_path, output_path):
    reader = PyPDF2.PdfReader(input_path)
    writer = PyPDF2.PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    with open(output_path, 'wb') as output_pdf:
        writer.write(output_pdf)

def optimize_text(input_path, output_path):
    with open(input_path, 'rb') as f_in:
        with gzip.open(output_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

def optimize_audio(input_path, output_path):
    audio = AudioSegment.from_file(input_path)
    audio.export(output_path, format="mp3", bitrate="64k")

def optimize_file(input_path, output_path, progress_bar, file_label, progress_frame, output_listbox):
    mime_type, _ = mimetypes.guess_type(input_path)
    if mime_type:
        progress_bar['value'] = 0
        file_label.config(text="Optimizing... 0%")
        progress_frame.pack()

        steps = 10
        step_progress = 100 / steps
        try:
            if mime_type.startswith('image/'):
                optimize_image(input_path, output_path)
            elif mime_type.startswith('video/'):
                optimize_video(input_path, output_path)
            elif mime_type == 'application/pdf':
                optimize_pdf(input_path, output_path)
            elif mime_type.startswith('text/'):
                optimize_text(input_path, output_path + '.gz')
            elif mime_type.startswith('audio/'):
                optimize_audio(input_path, output_path)
            else:
                file_label.config(text=f"Unsupported file type: {mime_type}")
                return False

            for i in range(steps):
                threading.Event().wait(0.5)
                progress_bar.step(step_progress)
                file_label.config(text=f"Optimizing... {int((i + 1) * step_progress)}%")
        except Exception as e:
            file_label.config(text=f"Error: {str(e)}")
            return False

        progress_bar['value'] = 100
        file_label.config(text="Optimization complete")
        progress_frame.pack_forget()

        optimized_folder = "Optimized Files"
        if not os.path.exists(optimized_folder):
            os.makedirs(optimized_folder)

        final_output_path = os.path.join(optimized_folder, os.path.basename(output_path))
        shutil.move(output_path, final_output_path)

        output_listbox.insert(END, final_output_path)

        return True
    else:
        file_label.config(text="Could not determine file type")
        return False

def start_optimization(input_path, progress_bar, file_label, progress_frame, output_listbox):
    optimized_folder = "Optimized Files"
    if not os.path.exists(optimized_folder):
        os.makedirs(optimized_folder)

    output_path = os.path.join(optimized_folder, os.path.basename(input_path))
    threading.Thread(target=optimize_file, args=(input_path, output_path, progress_bar, file_label, progress_frame, output_listbox)).start()
