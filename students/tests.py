from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Course, Department, Enrollment, Student


class StudentManagementTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='manager', password='test-password')
		self.department = Department.objects.create(name='Computer Science')
		self.student = Student.objects.create(student_id='STU001', first_name='Rahul', last_name='Sharma', email='rahul@example.com', department=self.department, enrollment_date=date.today())
		self.course = Course.objects.create(name='Programming', code='CS101', department=self.department)

	def test_student_creation(self):
		self.assertEqual(Student.objects.count(), 1)
		self.assertEqual(str(self.student), 'Rahul Sharma')

	def test_department_and_course_creation(self):
		self.assertEqual(str(self.department), 'Computer Science')
		self.assertEqual(str(self.course), 'CS101 - Programming')

	def test_enrollment_and_duplicate_prevention(self):
		Enrollment.objects.create(student=self.student, course=self.course)
		self.assertEqual(Enrollment.objects.count(), 1)
		with self.assertRaises(Exception):
			Enrollment.objects.create(student=self.student, course=self.course)

	def test_student_list_requires_authentication(self):
		response = self.client.get(reverse('student_list'))
		self.assertRedirects(response, f'{reverse("login")}?next={reverse("student_list")}')

	def test_authenticated_student_list_page(self):
		self.client.force_login(self.user)
		response = self.client.get(reverse('student_list'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Rahul Sharma')
