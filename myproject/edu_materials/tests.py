from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Course, Lesson
from users.models import User


class LessonUserTestCase(APITestCase):
    """Тесты для эндпоинтов лекций, если аутентифицирован простой пользователь,"""

    def setUp(self):
        """заполнение базы"""
        self.user = User.objects.create(email="user@user.ru")
        video_url = "https://www.youtube.com/"

        self.lesson = Lesson.objects.create(
            name="Test Lesson for tests",
            description="Test Lesson for tests",
            video_url=video_url,
            owner=self.user,
        )
        self.user2 = User.objects.create(email="user2@user.ru")
        self.lesson2 = Lesson.objects.create(
            name="Test Lesson for tests",
            description="Test Lesson for tests",
            video_url=video_url,
            owner=self.user2,
        )

        self.client.force_authenticate(user=self.user)

    def test_lesson_create(self):
        url = reverse("edu_materials:create_lesson")
        body = {"name": "Lesson 3"}
        request = self.client.post(url, body)

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 3)

    def test_lesson_list(self):
        """Тест на получение списка лекций"""

        video_url = reverse("edu_materials:lesson_list")
        response = self.client.get(video_url)
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
                    "course": None,
                    "description": self.lesson.description,
                    "preview": None,
                    "video_url": self.lesson.video_url,
                    "owner": self.user.pk,
                }
            ],
        }
        self.assertEqual(data, result)

    def test_lesson_retrieve(self):
        """Тест на корректное отображение детали лекции"""
        url = reverse("edu_materials:lesson_detail", args=(self.lesson.pk,))
        request = self.client.get(url)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get("name"), "Test Lesson for tests")
        self.assertEqual(response.get("owner"), self.user.pk)

    def test_lesson_retrieve_error(self):
        """Тест на некорректное отображение детали лекции"""
        url = reverse("edu_materials:lesson_detail", args=(self.lesson2.pk,))
        request = self.client.get(url)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.get("detail"), "You do not have permission to perform this action."
        )

    def test_lesson_update(self):
        """Тест на корректное редактирование лекции"""
        url = reverse("edu_materials:update_lesson", args=(self.lesson.pk,))
        body = {"name": "My Lesson"}
        request = self.client.patch(url, body)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get("name"), "My Lesson")

    def test_lesson_delete(self):
        """Тест на корректное удаление лекции"""
        url = reverse("edu_materials:delete_lesson", args=(self.lesson.pk,))
        request = self.client.delete(url)

        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 1)


class CourseSubscriptionTestCase(APITestCase):
    """Тесты на подписку на курс лекций"""

    def setUp(self):
        """заполнение базы"""
        self.user = User.objects.create(email="user@user.ru")
        self.course = Course.objects.create(name="Course 1", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_course_subscription(self):
        """Тест на успешную подписку на курс лекций"""
        url = reverse("edu_materials:course_subscription", args=(self.course.pk,))
        body = {"subscribe": True}
        request = self.client.post(url, body)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.get("message"), "Вы успешно подписаны на курс 'Course 1'"
        )

        url = reverse("edu_materials:course-detail", args=(self.course.pk,))
        request = self.client.get(url)
        response = request.json()

        self.assertTrue(response.get("is_subscribed"))

    def test_course_unsubscription(self):
        """Тест на успешную отмену подписки на курс лекций"""
        url = reverse("edu_materials:course_subscription", args=(self.course.pk,))
        body = {"subscribe": ""}
        request = self.client.post(url, body)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.get("message"), "Ваша подписка на курс 'Course 1' аннулирована."
        )
        url = reverse("edu_materials:course-detail", args=(self.course.pk,))
        request = self.client.get(url)
        response = request.json()

        self.assertFalse(response.get("is_subscribed"))


class CourseUserTestCase(APITestCase):
    """Тесты для эндпоинтов курса лекций, если аутентифицирован простой пользователь,"""

    def setUp(self):
        """заполнение базы"""
        self.user = User.objects.create(email="user@user.ru")
        self.course = Course.objects.create(name="Course 1", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_course_create(self):
        """Тесты на успешное создание курса лекций"""
        url = reverse("edu_materials:course-list")
        body = {"name": "Course 2"}
        request = self.client.post(url, body)

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_retrieve(self):
        """Тесты на успешное получение деталей о курсе лекций"""
        url = reverse("edu_materials:course-detail", args=(self.course.pk,))
        request = self.client.get(url)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get("name"), "Course 1")
        self.assertEqual(response.get("owner"), self.user.pk)

    def test_course_list(self):
        """Тесты на успешное создание списка курса лекций"""
        url = reverse("edu_materials:course-list")
        request = self.client.get(url)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response,
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.course.pk,
                        "name": self.course.name,
                        "description": None,
                        "owner": self.user.pk,
                        "amount_of_lessons": 0,
                        "lessons": [],
                        "is_subscribed": False,
                    }
                ],
            },
        )

    def test_course_update(self):
        """Тесты на успешное редактирование курса лекций"""
        url = reverse("edu_materials:course-detail", args=(self.course.pk,))
        body = {"name": "Мой курс"}
        request = self.client.patch(url, body)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get("name"), "Мой курс")

    def test_course_delete(self):
        """Тесты на успешное удаление курса лекций"""
        url = reverse("edu_materials:course-detail", args=(self.course.pk,))
        request = self.client.delete(url)

        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)


class CourseModeratorTestCase(APITestCase):
    """Тест для модераторов"""

    def setUp(self):
        """заполнение базы данных"""
        self.user = User.objects.create(email="user@user.ru")
        self.course = Course.objects.create(name="Course 1", owner=self.user)
        self.course2 = Course.objects.create(name="Course 2", owner=self.user)
        self.moder = User.objects.create(email="moder@moder.ru")
        self.moder.groups.create(name="moderators").save()
        self.client.force_authenticate(user=self.moder)

    def test_course_create_error(self):
        """Проверка, что модератор не вправе создать курс лекций"""
        url = reverse("edu_materials:course-list")
        body = {"name": "Moder Course"}
        request = self.client.post(url, body)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.get("detail"), "You do not have permission to perform this action."
        )
        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_list(self):
        """Проверка, что модератор может посмотреть список курсов лекций"""
        url = reverse("edu_materials:course-list")
        request = self.client.get(url)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response,
            {
                "count": 2,
                "next": "http://testserver/courses/?page=2",
                "previous": None,
                "results": [
                    {
                        "id": self.course.pk,
                        "name": self.course.name,
                        "description": None,
                        "owner": self.user.pk,
                        "amount_of_lessons": 0,
                        "lessons": [],
                        "is_subscribed": False,
                    }
                ],
            },
        )

    def test_course_update(self):
        """Проверка, что модератор может редактировать курс лекций"""
        url = reverse("edu_materials:course-detail", args=(self.course.pk,))
        body = {"name": "Moder Course"}
        request = self.client.patch(url, body)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get("name"), "Moder Course")

    def test_course_delete_error(self):
        """Проверка, что модератор не вправе удалить курс лекций"""
        url = reverse("edu_materials:course-detail", args=(self.course.pk,))
        request = self.client.delete(url)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.get("detail"), "You do not have permission to perform this action."
        )
        self.assertEqual(Course.objects.all().count(), 2)
