
import os
import shutil

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


def organize_folder(folder_path):

    preview = scan_folder(folder_path)

    moved_files = 0

    for file in preview:

        filename = file["filename"]
        category = file["category"]

        source = os.path.join(folder_path, filename)

        destination_folder = os.path.join(
            folder_path,
            category
        )

        os.makedirs(destination_folder, exist_ok=True)

        destination = os.path.join(
            destination_folder,
            filename
        )

        # Avoid overwriting existing files
        if os.path.exists(destination):
            continue

        shutil.move(source, destination)

        moved_files += 1

    return moved_files
