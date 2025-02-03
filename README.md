Features

    User Registration & Authentication: Register users, login, and manage profiles.
    Event Management: Admins can create, update, and delete events with associated venues and event dates.
    Event Enrollment: Users can enroll in events, and receive email confirmations.
    Email Notifications: Automated emails are sent for event creation and enrollment.
    Admin Panel: Admin interface to manage events, venues, and enrollments.

Technologies Used

    Django: Web framework for building the application.
    Django Rest Framework (DRF): Used for creating APIs for user registration, event enrollment, etc.
    Celery: For background task processing (e.g., sending emails).
    Redis: Message broker for Celery tasks.
    PostgreSQL: Database for storing event and user data.
    JWT (JSON Web Tokens): Authentication mechanism for APIs.
