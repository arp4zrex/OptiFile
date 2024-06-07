import os
import mimetypes
import shutil
import threading
import queue
from tkinter import END
import ffmpeg
import PyPDF2
import gzip
from pydub import AudioSegment
from pydub.utils import which
from PIL import Image, ImageSequence

AudioSegment.converter = which("ffmpeg")
AudioSegment.ffprobe = which("ffprobe")

def optimize_image(input_path, output_path):
    if input_path.lower().endswith('.gif'):
        optimize_gif(input_path, output_path)
    else:
        with Image.open(input_path) as img:
            img.save(output_path, optimize=True, quality=70)

def optimize_gif(input_path, output_path):
    with Image.open(input_path) as img:
        frames = ImageSequence.Iterator(img)
        frames = [frame.copy().convert("P", palette=Image.ADAPTIVE, colors=64).resize((frame.width // 2, frame.height // 2)) for frame in frames]
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            optimize=True,
            duration=img.info['duration'],
            loop=img.info.get('loop', 0)
        )

def optimize_video(input_path, output_path):
    try:
        (
            ffmpeg
            .input(input_path)
            .output(output_path, vcodec='libx264', crf=23, preset='medium')
            .run(overwrite_output=True)
        )
        print("Video optimized successfully")
    except ffmpeg.Error as e:
        print(f"Error optimizing video: {e.stderr.decode('utf-8')}")

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

def optimize_file(input_path, output_path, progress_bar, file_label, progress_frame, output_listbox, task_queue):
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
                task_queue.put({'progress': int((i + 1) * step_progress)})
        except Exception as e:
            file_label.config(text=f"Error: {str(e)}")
            return False

        task_queue.put(None)  # Signal that optimization is complete

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

def start_optimization(input_path, progress_bar, file_label, progress_frame, output_listbox, task_queue):
    output_path = os.path.join("Optimized Files", os.path.basename(input_path))
    thread = threading.Thread(target=optimize_file, args=(input_path, output_path, progress_bar, file_label, progress_frame, output_listbox, task_queue))
    thread.start()
    task_queue.put({'progress': 0})
