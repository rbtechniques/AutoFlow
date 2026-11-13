
import os

FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".pptx", ".xlsx"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi"],
    "Audio": [".mp3", ".wav", ".aac", ".flac"],
    "Archives": [".zip", ".rar", ".7z"],
    "Code": [".py", ".html", ".css", ".js", ".java", ".cpp"]
}


def get_category(extension):

    for category, extensions in FILE_CATEGORIES.items():

        if extension.lower() in extensions:
            return category

    return "Others"


def scan_folder(folder_path):

    if not os.path.isdir(folder_path):
        raise ValueError("The selected folder does not exist.")

    preview = []

    for filename in os.listdir(folder_path):

        source_path = os.path.join(folder_path, filename)

        # Ignore folders
        if os.path.isfile(source_path):

            extension = os.path.splitext(filename)[1]

            category = get_category(extension)

            preview.append({
                "filename": filename,
                "category": category,
                "source": source_path
            })

    return preview
