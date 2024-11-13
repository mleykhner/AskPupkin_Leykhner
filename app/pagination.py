from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginate(request, objects_list, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return page