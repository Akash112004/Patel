from django.db import models


class Department(models.Model):
	name = models.CharField(max_length=120, unique=True)
	description = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['name']

	def __str__(self):
		return self.name


class Student(models.Model):
	GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]

	student_id = models.CharField(max_length=30, unique=True)
	first_name = models.CharField(max_length=80)
	last_name = models.CharField(max_length=80)
	email = models.EmailField(unique=True)
	phone = models.CharField(max_length=30, blank=True)
	date_of_birth = models.DateField(null=True, blank=True)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
	address = models.TextField(blank=True)
	department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='students')
	enrollment_date = models.DateField()
	profile_image = models.ImageField(upload_to='students/', blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['last_name', 'first_name']

	def __str__(self):
		return f'{self.first_name} {self.last_name}'

	@property
	def full_name(self):
		return f'{self.first_name} {self.last_name}'


class Course(models.Model):
	name = models.CharField(max_length=150)
	code = models.CharField(max_length=30, unique=True)
	description = models.TextField(blank=True)
	credits = models.PositiveSmallIntegerField(default=3)
	department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='courses')
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['code']

	def __str__(self):
		return f'{self.code} - {self.name}'


class Enrollment(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
	course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
	enrollment_date = models.DateField(auto_now_add=True)

	class Meta:
		ordering = ['-enrollment_date']
		constraints = [models.UniqueConstraint(fields=['student', 'course'], name='unique_student_course')]

	def __str__(self):
		return f'{self.student} - {self.course.code}'
