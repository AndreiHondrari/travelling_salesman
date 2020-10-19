import time

from celery import exceptions as celery_exceptions
from celery.utils.log import get_task_logger

from jobs import constants, models
from optimisation_web.celery.app import app
from optimisation_web.celery.optimisation import optimisation_celery_app

logger = get_task_logger(__name__)

MAX_RETRIES = 10


@app.task
def calculate_shortest_path(job_id, locations, num_vehicles, depot):
    """Passes the call to the optimisation service and waits for a response"""

    # identify the job in the database
    try:
        job = models.Job.objects.get(id=job_id)
    except models.Job.DoesNotExist:
        logger.error(f"Could not retrieve job {job_id} from the database")
        return  # no need to do anything further

    # perform the call to the optimisation service worker
    task_response = optimisation_celery_app.send_task(
        'optimisation.calculate_shortest_path',
        (locations, num_vehicles, depot)
    )

    # attempt to retrieve result
    for i in range(MAX_RETRIES):
        if task_response.ready():
            try:
                result = task_response.get(timeout=5, disable_sync_subtasks=False)
                job.full_result = result
                job.status = constants.JobStatus.SUCCESSFUL if result else constants.JobStatus.FAILED
                job.save()
            except celery_exceptions.TimeoutError:
                job.status = constants.JobStatus.TIME_OUT
                logger.error(f"Could not retrieve result for job {job_id}")

            break

        time.sleep(1)

    job.status = constants.JobStatus.TIME_OUT
