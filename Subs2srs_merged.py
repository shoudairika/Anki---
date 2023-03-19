import os
from tkinter import filedialog, Tk, Button
import re
from datetime import datetime, timedelta

def merge_subtitles(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        blocks = re.split(r"\n\n", content.strip())
        subtitles = []

        for block in blocks:
            parts = block.split("\n")
            index = int(parts[0].strip())
            start_time, end_time = re.findall(r"(\d{2}:\d{2}:\d{2},\d{3})", parts[1])
            text = "\n".join(parts[2:])

            subtitles.append({
                "index": index,
                "start_time": datetime.strptime(start_time, "%H:%M:%S,%f"),
                "end_time": datetime.strptime(end_time, "%H:%M:%S,%f"),
                "text": text
            })

        merged_subtitles = [subtitles[0]]
        for i in range(1, len(subtitles)):
            time_diff = (subtitles[i]["start_time"] - merged_subtitles[-1]["end_time"]).total_seconds() * 1000

            if time_diff <= 90:
                merged_subtitles[-1]["end_time"] = subtitles[i]["end_time"]
                merged_subtitles[-1]["text"] += " " + subtitles[i]["text"]
            else:
                merged_subtitles.append(subtitles[i])

        output_file_path = os.path.splitext(file_path)[0] + "_merged.srt"
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            for i, subtitle in enumerate(merged_subtitles):
                output_file.write(f"{i + 1}\n")
                start_time = subtitle["start_time"].strftime("%H:%M:%S,%f")[:-3]
                end_time = subtitle["end_time"].strftime("%H:%M:%S,%f")[:-3]
                output_file.write(f"{start_time} --> {end_time}\n")
                output_file.write(f"{subtitle['text']}\n\n")

def process_files():
    file_paths = filedialog.askopenfilenames(filetypes=[("SRT files", "*.srt")])
    for file_path in file_paths:
        merge_subtitles(file_path)

root = Tk()
root.title("Subtitle Merger")
root.geometry("300x100")

select_button = Button(root, text="Select and Process SRT Files", command=process_files)
select_button.pack(expand=True, fill="both")

root.mainloop()
