from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from bookings.models import Booking
from .forms import ReviewForm
from .models import Review
from mechanics.models import Mechanic


@login_required
def review_list(request):

    reviews = Review.objects.all().order_by("-created_at")

    return render(
        request,
        "reviews/list.html",
        {
            "reviews": reviews,
        }
    )


@login_required
def add_review(request, mechanic_id):

    mechanic = get_object_or_404(
        Mechanic,
        id=mechanic_id
    )

    # Check if customer has a completed booking
    booking_exists = Booking.objects.filter(
        customer=request.user,
        mechanic=mechanic,
        status="Completed"
    ).exists()

    if not booking_exists:
        return render(
            request,
            "reviews/not_allowed.html",
            {
                "mechanic": mechanic,
            }
        )

    # Check if customer already reviewed this mechanic
    already_reviewed = Review.objects.filter(
        customer=request.user,
        mechanic=mechanic
    ).exists()

    if already_reviewed:
        return render(
            request,
            "reviews/already_reviewed.html",
            {
                "mechanic": mechanic,
            }
        )

    if request.method == "POST":

        form = ReviewForm(request.POST)

        if form.is_valid():

            review = form.save(commit=False)

            review.customer = request.user
            review.mechanic = mechanic

            review.save()

            # Recalculate mechanic rating
            reviews = Review.objects.filter(
                mechanic=mechanic
            )

            average = sum(
                review.rating
                for review in reviews
            ) / reviews.count()

            mechanic.rating = round(
                average,
                1
            )

            mechanic.save()

            return redirect(
                "mechanic_detail",
                id=mechanic.id
            )

    else:

        form = ReviewForm()

    return render(
        request,
        "reviews/add_review.html",
        {
            "form": form,
            "mechanic": mechanic,
        }
    )
