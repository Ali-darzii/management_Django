# management_Django
API Endpoints:

    /projects/ ---> CRUD operations for projects
    /tasks/ ---> CRUD operations for tasks
    /tasks/<id>/comments/ --> GET and CREATE operations for comments related to a specific task

Celery with RabbitMQ and Celery Beat:

    send_due_task_reminders: Sends an email reminder to users who have tasks due in 24 hours or less. This function will run once the Celery workers are up and will execute every 24 hours thereafter.
    daily_project_summary: Provides a summary of tasks for each project for the last 24 hours. This task runs daily.

WebSocket with Django Channels:

    /ws/notifications/: This endpoint does not work with Postman and static JavaScript due to CSRF token requirements. Instead, a WebSocket test page is available at [http://127.0.0.1:8000/ws_test/]. When connected, you can see the WebSocket connection in the console. You will receive notifications (logged in the console) for Task creation, update, deletion, and Comment creation and deletion. Don't forget to allow notifications.

Redis Caching for Celery:

    For Tasks and Projects, Redis caches the data in the list API with a 1-hour timeout to reduce PostgreSQL usage and provide faster responses.

I hope you enjoy using the app! 
    
