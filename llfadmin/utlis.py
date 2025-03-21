from django.core.paginator import Paginator
from django.contrib import messages

def check_is_superuser(user):
    if not user.is_authenticated or not user.is_superuser:
        return False
    return True


def make_paginator(request, list, no_items):
    paginator = Paginator(list, no_items)
    page_number = request.GET.get('page')
    if page_number:

        try:
            page_number = int(page_number)
            if page_number > paginator.num_pages:
                page_number = 1
                messages.error(
                    request, 'Page Not found going back to first page')
        except ValueError:
            messages.error(request, 'Not a valid page number')
            page_number = 1

    return paginator.get_page(page_number)
