from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Notification


@login_required
def notification_list(request):

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'notifications/list.html',
        {
            'notifications': notifications,
        }
    )


@login_required
def mark_notification_read(request, id):

    notification = get_object_or_404(
        Notification,
        id=id,
        user=request.user
    )

    notification.is_read = True
    notification.save()

    if notification.booking:
        return redirect(
            'booking_detail',
            id=notification.booking.id
        )

    return redirect(
        'notification_list'
    )


@login_required
def mark_all_read(request):

    Notification.objects.filter(
        user=request.user,
        is_read=False
    ).update(
        is_read=True
    )

    return redirect(
        'notification_list'
    )
