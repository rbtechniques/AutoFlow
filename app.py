

from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Temporary storage for workflows
workflows = []


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/workflows")
def workflow_page():
    return render_template("workflows.html", workflows=workflows)


@app.route("/create-workflow", methods=["POST"])
def create_workflow():

    name = request.form.get("name")
    description = request.form.get("description")
    workflow_type = request.form.get("type")

    workflow = {
        "name": name,
        "description": description,
        "type": workflow_type
    }

    workflows.append(workflow)

    return redirect("/workflows")


if __name__ == "__main__":
    app.run(debug=True)
