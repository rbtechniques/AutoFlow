

from organizer import organize_folder


def execute_workflow(workflow, folder_path=None):

    workflow_type = workflow["type"]

    if workflow_type == "File Management":

        if not folder_path:
            raise ValueError("Please provide a folder path.")

        moved_files = organize_folder(folder_path)

        return {
            "success": True,
            "message": f"Successfully organized {moved_files} files.",
            "files_processed": moved_files
        }

    elif workflow_type == "Productivity":

        return {
            "success": True,
            "message": "Productivity workflow execution recorded.",
            "files_processed": 0
        }

    else:
        raise ValueError("This workflow type is not supported yet.")
