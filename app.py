
from flask import Flask, render_template, request, redirect

from storage import init_db, add_workflow, get_workflows, add_history, get_history, get_dashboard_stats, get_workflow_by_id

from organizer import scan_folder

from organizer import scan_folder, organize_folder

from engine import execute_workflow


app = Flask(__name__)

# Create the database table if it doesn't exist
init_db()


@app.route("/")
def home():

    stats = get_dashboard_stats()

    return render_template(
        "index.html",
        stats=stats
    )


@app.route("/workflows")
def workflow_page():
    workflows = get_workflows()

    return render_template(
        "workflows.html",
        workflows=workflows
    )


@app.route("/create-workflow", methods=["POST"])
def create_workflow():

    name = request.form.get("name", "").strip()
    description = request.form.get("description", "").strip()
    workflow_type = request.form.get("type", "").strip()

    if not name or not description or not workflow_type:
        return redirect("/workflows")

    add_workflow(name, description, workflow_type)

    return redirect("/workflows")

@app.route("/organizer")
def organizer_page():
    return render_template("organizer.html", preview=None)


@app.route("/scan-folder", methods=["POST"])
def scan_folder_page():

    folder_path = request.form.get("folder_path", "").strip()

    try:
        preview = scan_folder(folder_path)

    except (ValueError, OSError):
        preview = []

    return render_template(
        "organizer.html",
        preview=preview,
        folder_path=folder_path
    )

@app.route("/organize-folder", methods=["POST"])
def organize_folder_page():

    folder_path = request.form.get("folder_path", "").strip()

    try:
        moved_files = organize_folder(folder_path)
        add_history(
        "File Organizer",
        f"Organized {moved_files} files successfully.",
        moved_files
        )

        return render_template(
            "organizer.html",
            preview=None,
            message=f"Successfully organized {moved_files} files!"
        )

    except (ValueError, OSError) as error:

        return render_template(
            "organizer.html",
            preview=None,
            error=str(error)
        )
@app.route("/history")
def history_page():

    history = get_history()

    return render_template(
        "history.html",
        history=history
    )


@app.route("/run-workflow", methods=["POST"])
def run_workflow_page():

    workflow_id = request.form.get("workflow_id")
    folder_path = request.form.get("folder_path", "").strip()

    try:
        workflow_id = int(workflow_id)
    except (TypeError, ValueError):
        return redirect("/workflows")

    workflow = get_workflow_by_id(workflow_id)

    if not workflow:
        return redirect("/workflows")

    try:
        result = execute_workflow(workflow, folder_path)

        add_history(
            f"Workflow: {workflow['name']}",
            result["message"],
            result["files_processed"]
        )

        return render_template(
            "workflows.html",
            workflows=get_workflows(),
            message=result["message"]
        )

    except (ValueError, OSError) as error:

        return render_template(
            "workflows.html",
            workflows=get_workflows(),
            error=str(error)
        )


if __name__ == "__main__":
    app.run(debug=True)
