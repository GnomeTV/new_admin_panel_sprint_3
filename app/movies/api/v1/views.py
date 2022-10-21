from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView
from django.http import Http404

from movies.models import Filmwork, PersonFilmwork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        print_fields = ['id', 'file_path', 'title', 'description',
                        'creation_date', 'rating', 'type']
        result = Filmwork.objects.values(*print_fields).annotate(
            genres=ArrayAgg(
                'genres__name',
                distinct=True
            ),
            actors=ArrayAgg(
                'persons__full_name',
                filter=Q(personfilmwork__role=PersonFilmwork.RoleTypes.actor),
                distinct=True
            ),
            directors=ArrayAgg(
                'persons__full_name',
                filter=Q(personfilmwork__role=PersonFilmwork.RoleTypes.director),
                distinct=True
            ),
            writers=ArrayAgg(
                'persons__full_name',
                filter=Q(personfilmwork__role=PersonFilmwork.RoleTypes.writer),
                distinct=True
            ),
        )
        return result

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    model = Filmwork
    http_method_names = ['get']
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )

        current_page = self.request.GET.get('page', 1)
        if current_page == 'last':
            current_page = paginator.num_pages
        else:
            try:
                current_page = int(current_page)
            except ValueError:
                raise Http404

        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': current_page - 1 if page.has_previous() else None,
            'next': current_page + 1 if page.has_next() else None,
            'results': list(queryset),
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    model = Filmwork
    http_method_names = ['get']

    def get_context_data(self, *, object_list=None, **kwargs):
        uuid = self.kwargs.get('pk')
        if not uuid:
            raise Http404
        queryset = self.get_queryset().filter(id=uuid)
        return queryset[0]
