from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.core.mail import send_mail
from .forms import ContactForm
from django.conf import settings

@ensure_csrf_cookie
def home(request):
    return render(request, "portfolio/index.html")

@require_POST
def contact_submit(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data["from_name"]
        email = form.cleaned_data["reply_to"]
        message = form.cleaned_data["message"]

        # 1. Send message to YOU
        send_mail(
            subject=f"Portfolio Contact | {name}",
            message=f"From: {name} <{email}>\n\n{message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["kowsalyacse1992@gmail.com"],  # your email
            fail_silently=False,
        )

        # 2. Auto-reply to sender
        send_mail(
            subject="Thank you for contacting me!",
            message=(
                f"Hi {name},\n\n"
                "Thank you for reaching out through my portfolio site.\n"
                "I have received your message and will get back to you soon.\n\n"
                "Best regards,\nKowsalya"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],  # sender's email
            fail_silently=False,
        )

        return JsonResponse({"ok": True})
    return JsonResponse({"ok": False, "errors": form.errors}, status=400)
