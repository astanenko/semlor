from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Bakery(models.Model):
    name = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    long = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.name


class Semlor(models.Model):
    SEMLOR_TYPES = (
        ("Classic", "Classic"),
        ("Wrap", "Wrap"),
        ("Coffee", "Coffee"),
        ("Vanilla", "Vanilla"),
    )

    bakery = models.ForeignKey(Bakery, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to="semlor_pictures/", blank=True)
    is_vegan = models.BooleanField(default=False)
    semlor_type = models.CharField(max_length=20, choices=SEMLOR_TYPES)
    price = models.FloatField()
    rating = models.FloatField(default=0)
    total_ratings = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bakery.name} {self.semlor_type}"


class Rating(models.Model):
    SEMLOR_RATINGS = [(i, str(i)) for i in range(1, 6)]

    semlor = models.ForeignKey(Semlor, on_delete=models.CASCADE, related_name="ratings")
    rating = models.IntegerField(choices=SEMLOR_RATINGS)
    comment = models.TextField(blank=True, max_length=1024)
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.semlor} {self.rating}"


@receiver(post_save, sender=Rating)
def update_semlor_rating(sender, instance, created, **kwargs):
    if created:
        semlor = instance.semlor
        ratings = semlor.ratings.all()
        total_ratings = len(ratings)
        total_score = sum(rating.rating for rating in ratings)
        semlor.rating = round(total_score / total_ratings) if total_ratings > 0 else 0
        semlor.total_ratings = total_ratings
        semlor.save()
