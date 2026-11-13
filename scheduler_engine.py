
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from storage import get_schedules, get_workflow_by_id, add_history
from engine import execute_workflow


scheduler = BackgroundScheduler(timezone="Asia/Kolkata")


def run_scheduled_workflow(schedule_id):

    schedules = get_schedules()

    schedule = next(
        (item for item in schedules if item["id"] == schedule_id),
        None
    )

    if not schedule or not schedule["is_active"]:
        return

    workflow = get_workflow_by_id(schedule["workflow_id"])

    if not workflow:
        return

    try:

        result = execute_workflow(
            workflow,
            schedule.get("folder_path")
        )

        add_history(
            f"Scheduled: {workflow['name']}",
            result["message"],
            result["files_processed"]
        )

    except Exception as error:

        add_history(
            f"Scheduled: {workflow['name']}",
            f"Execution failed: {error}",
            0
        )


def load_schedules():

    for schedule in get_schedules():

        if not schedule["is_active"]:
            continue

        schedule_id = schedule["id"]
        schedule_type = schedule["schedule_type"]

        if schedule_type == "Once":

            if not schedule["run_at"]:
                continue

            run_date = datetime.fromisoformat(
                schedule["run_at"]
            )

            if run_date <= datetime.now():
                continue

            scheduler.add_job(
                run_scheduled_workflow,
                trigger="date",
                run_date=run_date,
                args=[schedule_id],
                id=f"schedule_{schedule_id}",
                replace_existing=True
            )

        elif schedule_type == "Daily":

            scheduler.add_job(
                run_scheduled_workflow,
                trigger="cron",
                hour=int(schedule["run_time"][:2]),
                minute=int(schedule["run_time"][3:5]),
                args=[schedule_id],
                id=f"schedule_{schedule_id}",
                replace_existing=True
            )

        elif schedule_type == "Weekly":

            scheduler.add_job(
                run_scheduled_workflow,
                trigger="cron",
                day_of_week=schedule["day_of_week"],
                hour=int(schedule["run_time"][:2]),
                minute=int(schedule["run_time"][3:5]),
                args=[schedule_id],
                id=f"schedule_{schedule_id}",
                replace_existing=True
            )


def start_scheduler():

    if not scheduler.running:

        load_schedules()
        scheduler.start()

def refresh_schedules():

    if scheduler.running:

        scheduler.remove_all_jobs()

        load_schedules()