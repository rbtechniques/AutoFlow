
from flask import Flask, render_template, request, redirect

from storage import init_db, add_workflow, get_workflows

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


if __name__ == "__main__":
    app.run(debug=True)
