import os
from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone

scheduler = None
class ContractConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contract'

    def ready(self):
        print("Entered ready()")
        from django.conf import settings

        if settings.DEBUG and os.environ.get('RUN_MAIN') != 'true':
            print("Skipping scheduler because RUN_MAIN != 'true'")
            return
        
        print("Starting scheduler...")
        
        from .scheduler import send_expiration_email
        
        scheduler = BackgroundScheduler(timezone=str(timezone.get_current_timezone()))
        scheduler.add_job(
            send_expiration_email,
            'interval',           
            minutes=1,            
            next_run_time=timezone.now() 
        )
        scheduler.start()
        print("✅ APScheduler started, running every minute...")