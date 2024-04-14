import logging
from django.shortcuts import render
from .tasks import simple_task_1, simple_task_2
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from django.db import connection
import time
import psutil

def index(request):
    return render(request, 'index.html')


logger = logging.getLogger(__name__)


def view1(request):
    logger.info('Starting view1()')
    if request.method == 'POST':
        simple_task_1.delay()
        logger.info('Finished view1()')
        return render(request, 'index.html', context={'button1': True})


def view2(request):
    logger.info('Starting view2()')
    if request.method == 'POST':
        simple_task_2.delay()
        logger.info('Finished view2()')
        return render(request, 'index.html', context={'button2': True})

@require_GET
def health_check(request):
    health_status = {'status': 'OK'}

    # 1. Checking database connection status
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
    except Exception as e:
        return JsonResponse({'status': 'Database connection error'}, status=500)

    # 2. Measuring database response time
    try:
        start_time = time.time()
        cursor.execute("SELECT 1")
        health_status['database_response_time'] = time.time() - start_time
    except Exception as e:
        return JsonResponse({'status': 'Database response time measurement error'}, status=500)

    # 3. Checking memory consumptionb
    memory_usage = psutil.virtual_memory().percent
    health_status['memory_usage'] = memory_usage
    if memory_usage > 90:  # Example threshold of memory usage considered dangerous
        health_status['status'] = 'High memory usage'
        health_status['memory_usage'] = memory_usage
        return JsonResponse(health_status, status=500)

    

    # 5. Checking the status of other API dependencies
    # Here you can put code to check the status of other external API dependencies

    return JsonResponse(health_status)