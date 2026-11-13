
from flask import Flask, render_template, request, redirect

from storage import init_db, add_workflow, get_workflows

from organizer import scan_folder

from organizer import scan_folder, organize_folder

app = Flask(__name__)

# Create the database table if it doesn't exist
init_db()


@app.route("/")
def home():
    return render_template("index.html")


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

if __name__ == "__main__":
    app.run(debug=True)
