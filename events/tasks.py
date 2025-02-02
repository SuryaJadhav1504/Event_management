from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings

@shared_task
def send_event_creation_email(event_name):
    try:
        # Print the received event name
        print(f"Sending email for event: {event_name}")

        # Get all users
        users = User.objects.all()

        subject = f"New Event Created: {event_name}"
        message = f"A new event has been created- {event_name}. Check it out!"
        
        # Send email to all users
        for user in users:
            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                )
                print(f"Email sent to {user.email}")
            except Exception as e:
                print(f"Failed to send email to {user.email}: {str(e)}")

        print(f"Emails successfully sent to {len(users)} users.")
        return f"Emails successfully sent to {len(users)} users."

    except Exception as e:
        print(f"Error in sending event creation email: {str(e)}")
        return f"Error: {str(e)}"



@shared_task
def send_enrollment_confirmation_email(event_name, user_email):
    try:
        # Print the received event name and user email
        print(f"Sending enrollment confirmation email for event: {event_name} to {user_email}")

        subject = f"Event Enrollment Confirmation: {event_name}"
        message = f"You have successfully enrolled in the event: {event_name}. We look forward to your participation!"

        # Send email only to the enrolled user
        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,  # Ensure this is correctly set up in settings.py
                [user_email],  # Send the email to the user who enrolled
            )
            print(f"Email sent to {user_email}")
        except Exception as e:
            print(f"Failed to send email to {user_email}: {str(e)}")

        return f"Email successfully sent to {user_email}."

    except Exception as e:
        print(f"Error in sending enrollment confirmation email: {str(e)}")
        return f"Error: {str(e)}"