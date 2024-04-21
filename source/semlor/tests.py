import secrets
import string

from django.urls import reverse
from django.test import TestCase
from semlor.models import City, Bakery, Semlor, Rating


class SemlorTests(TestCase):
    def setUp(self):
        city, created = City.objects.get_or_create(name="Gotham City")

        bakery, created = Bakery.objects.get_or_create(
            name="Acme Corporation",
            city=city,
            address="Gotham City",
            lat=0,
            long=0,
        )

        self.semlor = Semlor.objects.create(
            bakery=bakery,
            is_vegan=True,
            semlor_type="Classic",
            price=float(10),
        )
        self.semlor_name = str(self.semlor)

    def tearDown(self):
        self.semlor.delete()

    def test_detail_view(self):
        response = self.client.get(
            reverse("semlor_detail", args=[self.semlor.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.semlor_name)
        self.assertContains(response, "<strong>Rating:</strong> 0")

    def test_semlor_list_view(self):
        url = reverse("semlor_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.semlor_name)

    def test_add_rating(self):
        rating_count_before = Rating.objects.count()
        url = reverse("semlor_detail", args=[self.semlor.id])
        data = {
            "semlor": self.semlor.id,
            "rating": 5,
            "comment": "Great semlor!",
        }
        response = self.client.post(url, data, headers={"User-Agent": "Tests"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Rating.objects.count(), rating_count_before + 1)

        response = self.client.get(
            reverse("semlor_detail", args=[self.semlor.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<strong>Rating:</strong> 5")

    def test_rating_avg(self):
        url = reverse("semlor_detail", args=[self.semlor.id])
        total = 0
        for i in range(1, 6):
            total += i
            data = {"rating": i, "comment": "Contradictory semlor!"}
            response = self.client.post(
                url, data, headers={"User-Agent": "Tests"}
            )
            self.assertEqual(response.status_code, 302)

        response = self.client.get(
            reverse("semlor_detail", args=[self.semlor.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, f"<strong>Rating:</strong> {round(total / 5)}"
        )

    def test_rating_limit(self):
        url = reverse("semlor_detail", args=[self.semlor.id])
        for _ in range(5):
            data = {"rating": 5, "comment": "Great semlor!"}
            response = self.client.post(
                url, data, headers={"User-Agent": "Tests"}
            )
            self.assertEqual(response.status_code, 302)

        rating_count_before = Rating.objects.count()
        # Try to add another rating, which should fail
        data = {
            "semlor": self.semlor.id,
            "rating": 5,
            "comment": "Great semlor!",
        }
        response = self.client.post(url, data, headers={"User-Agent": "Tests"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "text-danger")
        self.assertEqual(rating_count_before, Rating.objects.count())

    def test_valid_invalid_ratings(self):
        url = reverse("semlor_detail", args=[self.semlor.id])
        valid_data = {"rating": 5, "comment": "Great semlor!"}
        valid_response = self.client.post(
            url, valid_data, headers={"User-Agent": "Tests"}
        )
        self.assertEqual(valid_response.status_code, 302)
        rating_count_before = Rating.objects.count()

        # Add an invalid rating
        invalid_data = {"rating": 6, "comment": "Invalid rating!"}
        invalid_response = self.client.post(
            url, invalid_data, headers={"User-Agent": "Tests"}
        )
        self.assertContains(invalid_response, "text-danger")
        self.assertEqual(rating_count_before, Rating.objects.count())

        # Add an invalid comment
        comment = "".join(
            secrets.choice(string.ascii_letters + string.digits)
            for _ in range(2000)
        )
        invalid_data = {"rating": 5, "comment": comment}
        invalid_response = self.client.post(
            url, invalid_data, headers={"User-Agent": "Tests"}
        )
        self.assertContains(invalid_response, "text-danger")
        self.assertEqual(rating_count_before, Rating.objects.count())
