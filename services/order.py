from django.db import transaction
from db.models import Order, Ticket, User

def create_order(tickets: list[dict], username: str, date: str | None = None) -> Order:
    user = User.objects.get(username=username)

    with transaction.atomic():
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
            )

    return order


def get_orders(username: str | None = None):
    if username:
        return Order.objects.filter(user__username=username).order_by("-created_at")
    return Order.objects.all().order_by("-user__username")
