from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import DetailView

from .forms import RatingForm
from django.shortcuts import render
from .models import Semlor


class SemlorListView(View):
    def get(self, request):
        top_semlors = Semlor.objects.order_by("-rating")[:3]
        other_semlors = Semlor.objects.exclude(
            id__in=[semlor.id for semlor in top_semlors]
        ).order_by("-rating")

        return render(
            request,
            "semlor/semlor_list.html",
            {"top_semlors": top_semlors, "other_semlors": other_semlors},
        )


class SemlorDetailView(DetailView):
    model = Semlor
    template_name = "semlor/semlor_detail.html"
    context_object_name = "semlor"

    def get_object(self, queryset=None):
        semlor_id = self.kwargs.get("semlor_id")
        return get_object_or_404(Semlor, pk=semlor_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rating_form"] = RatingForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        rating_form = RatingForm(
            request.POST,
            ip_address=request.META.get("REMOTE_ADDR"),
            user_agent=request.META.get("HTTP_USER_AGENT"),
        )
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.semlor = self.object
            rating.save()
            messages.success(request, "Thank you! Your rating has been added.")
            return redirect("semlor_detail", semlor_id=self.object.pk)
        else:
            context = self.get_context_data()
            context["rating_form"] = rating_form
            return self.render_to_response(context)
