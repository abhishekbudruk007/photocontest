from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


def send_mail(to, template, context):
    html_content = render_to_string(f'accounts/emails/{template}.html', context)
    text_content = render_to_string(f'accounts/emails/{template}.txt', context)

    msg = EmailMultiAlternatives(context['subject'], text_content, settings.EMAIL_HOST_USER, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()



def send_activation_email(request, email, code):
    context = {
        'subject': _('Profile activation'),
        'uri': request.build_absolute_uri(reverse('accounts:activate', kwargs={'code': code})),
    }

    send_mail(email, 'activate_profile', context)


def send_activation_change_email(request, email, code):
    context = {
        'subject': _('Change email'),
        'uri': request.build_absolute_uri(reverse('accounts:change_email_activation', kwargs={'code': code})),
    }

    send_mail(email, 'change_email', context)

def send_mail_to_winner(winner_list, email):
    print("winner_list",winner_list)
    context = {
        'subject': 'Congratulations- Winners of Photocontest',
        'first_name': winner_list.participant_id.participant_user.first_name,
        'last_name': winner_list.participant_id.participant_user.last_name,
        'contest_name': winner_list.participant_contest.contest_name,
        # 'uri': request.build_absolute_uri(reverse('accounts:change_email_activation', kwargs={'code': code})),
    }

    send_mail(email, 'winner_of_photocontest', context)


def send_reset_password_email(request, email, token, uid):
    context = {
        'subject': _('Restore password'),
        'uri': request.build_absolute_uri(
            reverse('accounts:restore_password_confirm', kwargs={'uidb64': uid, 'token': token})),
    }

    send_mail(email, 'restore_password_email', context)


def send_forgotten_username_email(email, username):
    context = {
        'subject': _('Your username'),
        'username': username,
    }

    send_mail(email, 'forgotten_username', context)
