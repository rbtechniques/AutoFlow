
from flask import Flask, render_template, request, redirect

from storage import init_db, add_workflow, get_workflows, add_history, get_history, get_dashboard_stats, get_workflow_by_id, add_schedule, get_schedules

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

@app.route("/add-schedule", methods=["POST"])
def add_schedule_page():

    workflow_id = request.form.get("workflow_id")
    schedule_type = request.form.get("schedule_type")
    run_at = request.form.get("run_at")
    run_time = request.form.get("run_time")
    day_of_week = request.form.get("day_of_week")

    try:
        workflow_id = int(workflow_id)

        if not get_workflow_by_id(workflow_id):
            raise ValueError("Selected workflow does not exist!")
        if schedule_type == "Once":
            if not run_at:
                raise ValueError("Please provide a date and time for schedule.")
            add_schedule(
               workflow_id,
               schedule_type,
               run_at=run_at
           ) 
        elif schedule_type == "Daily":
            if not run_time:
                raise ValueError("Please provide a time for daily schedule.")
            add_schedule(
                workflow_id,
                schedule_type,
                run_time=run_time
            )
        elif schedule_type == "Weekly":
            if not run_time or not day_of_week:
                raise ValueError("Please provide a time and day for weekly schedule.")
            add_schedule(
                workflow_id,
                schedule_type,
                run_time=run_time,
                day_of_week=day_of_week
            )
        else:
            raise ValueError("Invalid schedule type selected.")
        return redirect("/scheduler")
    except (TypeError, ValueError) as error:
        return render_template(
            "scheduler.html",
            workflows=get_workflows(),
            schedules=get_schedules(),
            error=str(error)
        )

    workflow = get_workflow_by_id(workflow_id)

    if not workflow:
        return redirect("/scheduler")

    add_schedule(workflow_id, schedule_type, run_at, run_time, day_of_week)

    return redirect("/scheduler")

@app.route("/scheduler")
def scheduler_page():

    return render_template(
        "scheduler.html",
        workflows=get_workflows(),
        schedules=get_schedules()
    )

if __name__ == "__main__":
    app.run(debug=True)
