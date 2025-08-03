# --- Cron Job Scheduler Setup ---

import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Import the tasks that the scheduler will run
from .tasks import (
    run_automated_publishing_job,
    run_viral_intelligence_job,
    run_performance_metrics_sync_job,
    run_oauth_refresh_job
)
from ..utils.database import JSONDatabase

logger = logging.getLogger(__name__)

def create_scheduler(db: JSONDatabase, encrypt_func, decrypt_func) -> AsyncIOScheduler:
    """
    Creates, configures, and returns the scheduler instance with all jobs defined.
    """
    scheduler = AsyncIOScheduler()

    logger.info("Adding cron jobs to the scheduler...")

    # Job 1: Automated Content Publishing (every minute)
    scheduler.add_job(
        run_automated_publishing_job,
        'interval',
        minutes=1,
        args=[db, decrypt_func]
    )

    # Job 2: Viral Intelligence Harvesting (every 6 hours)
    scheduler.add_job(
        run_viral_intelligence_job,
        'interval',
        hours=6,
        args=[db]
    )

    # Job 3: Performance Metrics Sync (every 24 hours)
    scheduler.add_job(
        run_performance_metrics_sync_job,
        'interval',
        hours=24,
        args=[db, decrypt_func]
    )

    # Job 4: OAuth Token Auto-Refresh (every hour)
    scheduler.add_job(
        run_oauth_refresh_job,
        'interval',
        hours=1,
        args=[db, encrypt_func, decrypt_func]
    )

    logger.info("All cron jobs have been added.")
    return scheduler
