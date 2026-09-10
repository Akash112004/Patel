from django.contrib import admin

from .models import Course, Department, Enrollment, Student


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
	list_display = ['name', 'created_at']
	search_fields = ['name']
	ordering = ['name']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
	list_display = ['student_id', 'full_name', 'email', 'department', 'enrollment_date']
	search_fields = ['student_id', 'first_name', 'last_name', 'email']
	list_filter = ['department', 'gender']
	ordering = ['last_name', 'first_name']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
	list_display = ['code', 'name', 'department', 'credits']
	search_fields = ['code', 'name']
	list_filter = ['department', 'credits']
	ordering = ['code']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
	list_display = ['student', 'course', 'enrollment_date']
	search_fields = ['student__student_id', 'student__last_name', 'course__code', 'course__name']
	list_filter = ['course__department', 'enrollment_date']
	ordering = ['-enrollment_date']
