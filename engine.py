
from organizer import scan_folder


def execute_workflow(workflow, folder_path=None):

    workflow_type = workflow["type"]

    # File Management workflow
    if workflow_type == "File Management":

        if not folder_path:
            raise ValueError("Please provide a folder path.")

        files = scan_folder(folder_path)

        return {
            "success": True,
            "message": f"Successfully scanned {len(files)} files.",
            "files_processed": len(files)
        }

    # Productivity workflow
    elif workflow_type == "Productivity":

        return {
            "success": True,
            "message": "Productivity workflow execution recorded.",
            "files_processed": 0
        }

    else:
        raise ValueError(
            "This workflow type is not supported yet."
        )
