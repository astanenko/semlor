from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Rating


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["rating", "comment"]
        labels = {"rating": "Rating", "comment": "Comment"}
        widgets = {
            "rating": forms.Select(attrs={"class": "form-control"}),
            "comment": forms.Textarea(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        self.ip_address = kwargs.pop("ip_address", None)
        self.user_agent = kwargs.pop("user_agent", None)
        super(RatingForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        if not self.user_agent or not self.ip_address:
            raise ValidationError({"rating": "Something went wrong"})

        if (
            Rating.objects.filter(
                ip_address=self.ip_address,
                user_agent=self.user_agent,
                created_at__date=timezone.now().date(),
            ).count()
            >= 5
        ):
            raise ValidationError(
                {
                    "rating": "Max votes per day reached. Try again tomorrow"
                }
            )

        return cleaned_data

    def save(self, commit=True):
        instance = super(RatingForm, self).save(commit=False)
        instance.ip_address = self.ip_address
        instance.user_agent = self.user_agent
        if commit:
            instance.save()
        return instance
