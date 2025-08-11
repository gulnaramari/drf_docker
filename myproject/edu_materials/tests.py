from rest_framework.fields import DateTimeField
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from .models import Course, Lesson
from users.models import User


class TestCase(APITestCase):
    """Базовый тестовый класс для всех тестов."""

    def setUp(self):
        """Задает начальные данные для тестов."""

        self.user = User.objects.create(email="admin@sky.pro")
        video_url = "https://www.youtube.com/"
        self.course = Course.objects.create(
            name="Test Course for tests",
            description="Test Course for tests",
            owner=self.user,
        )
        self.lesson = Lesson.objects.create(
            name="Test Lesson for tests",
            description="Test Lesson for tests",
            course=self.course,
            video_url=video_url,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)


class CourseTestCase(TestCase, APITestCase):
    def test_course_list(self):
        res_created_at = DateTimeField().to_representation
        res_updated_at = DateTimeField().to_representation
        url = reverse("edu_materials:courses-list")
        response = self.client.get(url)
        data = response.json()

        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "amount_of_lessons": 1,
                    "lesson": [
                        {
                            "id": self.lesson.pk,
                            "name": self.lesson.name,
                            "description": self.lesson.description,
                            "preview": None,
                            "video_url": self.lesson.video_url,
                            "course": self.course.pk,
                            "owner": self.user.pk,
                            "created_at": res_created_at(self.lesson.created_at),
                            "updated_at": res_updated_at(self.lesson.updated_at),
                        }
                    ],
                    "is_subscribed": False,
                    "count_subscriptions": "Подписок - 0.",
                    "name": self.course.name,
                    "preview": None,
                    "description": self.course.description,
                    "owner": self.user.pk,
                    "created_at": res_created_at(self.course.created_at),
                    "updated_at": res_updated_at(self.course.updated_at),
                }
            ],
        }
        if response.status_code != status.HTTP_200_OK:
            print("COURSE LIST ERRORS:", response.status_code, response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_retrieve_course(self):
        """Тест получения курса по Primary Key."""
        url = reverse("edu_materials:courses-detail", args=[self.course.pk])
        response = self.client.get(url)
        data = response.json()
        if response.status_code != status.HTTP_200_OK:
            print("COURSE RETRIEVE ERRORS:", response.status_code, response.json())
        data = response.json()
        self.assertEqual(Course.objects.all().count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.course.name)

    def test_create_course(self):
        """Тест создания нового курса."""

        url = reverse("edu_materials:courses-list")
        data = {
            "name": "Test Course for tests 2",
            "description": "Test Course for tests 2",
            "owner": self.user.pk,
        }
        response = self.client.post(url, data=data)
        if response.status_code != status.HTTP_201_CREATED:
            print("COURSE CREATE ERRORS:", response.status_code, response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Course.objects.filter(name="Test Course for tests 2").count(), 1
        )
        self.assertTrue(Course.objects.all().exists())

    def test_update_course(self):
        """Тест изменения курса по Primary Key."""

        url = reverse("edu_materials:courses-detail", args=(self.course.pk,))
        data = {
            "name": "Updated Test Course for tests",
            "description": "Updated Test Course for tests",
        }
        response = self.client.put(url, data=data)
        if response.status_code != status.HTTP_200_OK:
            print("COURSE UPDATE ERRORS:", response.status_code, response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Course.objects.get(pk=self.course.pk).name, "Updated Test Course for tests"
        )

    def test_delete_course(self):
        """Тест удаления курса по Primary Key."""

        url = reverse("edu_materials:courses-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        if response.status_code != status.HTTP_204_NO_CONTENT:
            print("COURSE DELETE ERRORS:", response.status_code, response.json())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)


class LessonTestCase(TestCase, APITestCase):
    """Тесты для работы с уроками."""

    def test_lesson_list(self):
        """Тест на получение списка уроков."""
        res_created_at = DateTimeField().to_representation
        res_updated_at = DateTimeField().to_representation

        url = reverse("edu_materials:lesson_list")
        response = self.client.get(url)
        if response.status_code != status.HTTP_200_OK:
            print("LESSON LIST ERRORS:", response.status_code, response.json())
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "name": self.lesson.name,
                    "description": self.lesson.description,
                    "preview": None,
                    "video_url": self.lesson.video_url,
                    "created_at": res_created_at(self.lesson.created_at),
                    "updated_at": res_updated_at(self.lesson.updated_at),
                    "course": self.course.pk,
                    "owner": self.user.pk,
                }
            ],
        }
        self.assertEqual(data, result)

    def test_retrieve_lesson(self):
        """Тест получения урока по Primary Key."""

        url = reverse("edu_materials:lesson_detail", args=(self.lesson.pk,))
        response = self.client.get(url)
        if response.status_code != status.HTTP_200_OK:
            print("LESSON RETRIEVE ERRORS:", response.status_code, response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["name"], self.lesson.name)

        print(response.status_code)
        print(response.json())

    def test_create_lesson(self):
        url = reverse("edu_materials:create_lesson")
        data = {
            "name": "Test Lesson for tests 2",
            "description": "Test Lesson for tests 2",
            "video_url": "https://www.youtube.com/lesson_1",
            "course": self.course.pk,
            "owner": self.user.pk,
        }
        response = self.client.post(url, data=data)
        if response.status_code != status.HTTP_201_CREATED:
            print("LESSON CREATE ERRORS:", response.status_code, response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Lesson.objects.filter(description="Test Lesson for tests 2").count(), 1
        )
        self.assertTrue(Lesson.objects.all().exists())

    def test_update_lesson(self):
        url = reverse("edu_materials:update_lesson", args=(self.lesson.pk,))
        data = {
            "name": "Updated Test Lesson for tests",
            "description": "Updated Test Lesson for tests 2",
            "video_url": "https://www.youtube.com/lesson_1",
            "course": self.course.pk,
            "owner": self.user.pk,
        }
        response = self.client.put(url, data=data)
        if response.status_code != status.HTTP_200_OK:
            print("LESSON UPDATE ERRORS:", response.status_code, response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Lesson.objects.get(pk=self.lesson.pk).description,
            "Updated Test Lesson for tests 2",
        )

    def test_lesson_delete(self):
        url = reverse("edu_materials:delete_lesson", args=(self.lesson.pk,))
        response = self.client.delete(url)
        if response.status_code != status.HTTP_204_NO_CONTENT:
            print("LESSON DELETE ERRORS:", response.status_code, response.json())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)
