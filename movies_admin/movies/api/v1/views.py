from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.list import BaseListView 
from django.views.generic.detail import BaseDetailView

from movies.models import Filmwork, PersonRole


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def _aggregate_person(self, role):
        return ArrayAgg('persons__full_name', distinct=True, filter=Q(personfilmwork__role=role))

    def get_queryset(self):
        return Filmwork.objects.prefetch_related('genres', 'persons').values().annotate(
            genres=ArrayAgg(
                'genres__name', 
                distinct=True
                )
            ).annotate(
                actors=self._aggregate_person(PersonRole.ACTOR)
                ).annotate(
                    directors=self._aggregate_person(PersonRole.DIRECTOR)
                    ).annotate(
                        writers=self._aggregate_person(PersonRole.WRITER)
                        )

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class Movies(MoviesApiMixin, BaseListView):
    paginate_by = 50
    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, _ = self.paginate_queryset(
            queryset, 
            self.paginate_by
        )
        next = page.next_page_number() if page.has_next() else None
        prev = page.previous_page_number() if page.has_previous() else None

        context = {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "prev": prev,
            "next": next,
            "results": list(page.object_list),
        }
        return context
                

class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_context_data(self, **kwargs):
        return self.get_queryset().get(id=kwargs['object']['id'])