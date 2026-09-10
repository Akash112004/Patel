from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CourseForm, DepartmentForm, EnrollmentForm, StudentForm
from .models import Course, Department, Enrollment, Student


@login_required
def dashboard(request):
	return render(request, 'students/dashboard.html', {
		'student_count': Student.objects.count(), 'department_count': Department.objects.count(),
		'course_count': Course.objects.count(), 'enrollment_count': Enrollment.objects.count(),
		'recent_students': Student.objects.select_related('department').order_by('-created_at')[:5],
		'recent_courses': Course.objects.select_related('department').order_by('-created_at')[:5],
	})


@login_required
def student_list(request):
	students = Student.objects.select_related('department')
	query = request.GET.get('q', '').strip()
	department_id = request.GET.get('department', '')
	if query:
		students = students.filter(Q(student_id__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(email__icontains=query))
	if department_id:
		students = students.filter(department_id=department_id)
	page = Paginator(students, 10).get_page(request.GET.get('page'))
	return render(request, 'students/student_list.html', {'page': page, 'departments': Department.objects.all(), 'query': query, 'selected_department': department_id})


@login_required
def student_detail(request, pk):
	student = get_object_or_404(Student.objects.select_related('department').prefetch_related('enrollments__course'), pk=pk)
	return render(request, 'students/student_detail.html', {'student': student})


@login_required
def student_create(request):
	form = StudentForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		form.save(); messages.success(request, 'Student added successfully.'); return redirect('student_list')
	return render(request, 'students/form.html', {'form': form, 'title': 'Add student', 'back_url': 'student_list'})


@login_required
def student_update(request, pk):
	student = get_object_or_404(Student, pk=pk)
	form = StudentForm(request.POST or None, request.FILES or None, instance=student)
	if form.is_valid():
		form.save(); messages.success(request, 'Student updated successfully.'); return redirect('student_detail', pk=pk)
	return render(request, 'students/form.html', {'form': form, 'title': 'Edit student', 'back_url': 'student_detail', 'back_pk': pk})


@login_required
def student_delete(request, pk):
	student = get_object_or_404(Student, pk=pk)
	if request.method == 'POST':
		student.delete(); messages.success(request, 'Student deleted successfully.'); return redirect('student_list')
	return render(request, 'students/confirm_delete.html', {'object': student, 'object_type': 'student', 'cancel_url': 'student_detail', 'cancel_pk': pk})


@login_required
def department_list(request):
	return render(request, 'students/department_list.html', {'departments': Department.objects.all()})


@login_required
def department_detail(request, pk):
	return render(request, 'students/department_detail.html', {'department': get_object_or_404(Department.objects.prefetch_related('students', 'courses'), pk=pk)})


@login_required
def department_create(request):
	form = DepartmentForm(request.POST or None)
	if form.is_valid():
		form.save(); messages.success(request, 'Department added successfully.'); return redirect('department_list')
	return render(request, 'students/form.html', {'form': form, 'title': 'Add department', 'back_url': 'department_list'})


@login_required
def department_update(request, pk):
	department = get_object_or_404(Department, pk=pk); form = DepartmentForm(request.POST or None, instance=department)
	if form.is_valid():
		form.save(); messages.success(request, 'Department updated successfully.'); return redirect('department_detail', pk=pk)
	return render(request, 'students/form.html', {'form': form, 'title': 'Edit department', 'back_url': 'department_detail', 'back_pk': pk})


@login_required
def department_delete(request, pk):
	department = get_object_or_404(Department, pk=pk)
	if request.method == 'POST':
		try:
			department.delete(); messages.success(request, 'Department deleted successfully.'); return redirect('department_list')
		except Exception:
			messages.error(request, 'This department cannot be deleted while it has students or courses.'); return redirect('department_detail', pk=pk)
	return render(request, 'students/confirm_delete.html', {'object': department, 'object_type': 'department', 'cancel_url': 'department_detail', 'cancel_pk': pk})


@login_required
def course_list(request):
	courses = Course.objects.select_related('department'); query = request.GET.get('q', '').strip()
	if query: courses = courses.filter(Q(name__icontains=query) | Q(code__icontains=query))
	return render(request, 'students/course_list.html', {'courses': courses, 'query': query})


@login_required
def course_create(request):
	form = CourseForm(request.POST or None)
	if form.is_valid():
		form.save(); messages.success(request, 'Course added successfully.'); return redirect('course_list')
	return render(request, 'students/form.html', {'form': form, 'title': 'Add course', 'back_url': 'course_list'})


@login_required
def course_update(request, pk):
	course = get_object_or_404(Course, pk=pk); form = CourseForm(request.POST or None, instance=course)
	if form.is_valid():
		form.save(); messages.success(request, 'Course updated successfully.'); return redirect('course_list')
	return render(request, 'students/form.html', {'form': form, 'title': 'Edit course', 'back_url': 'course_list'})


@login_required
def course_delete(request, pk):
	course = get_object_or_404(Course, pk=pk)
	if request.method == 'POST':
		course.delete(); messages.success(request, 'Course deleted successfully.'); return redirect('course_list')
	return render(request, 'students/confirm_delete.html', {'object': course, 'object_type': 'course', 'cancel_url': 'course_list'})


@login_required
def enrollment_list(request):
	return render(request, 'students/enrollment_list.html', {'enrollments': Enrollment.objects.select_related('student', 'course')})


@login_required
def enrollment_create(request):
	form = EnrollmentForm(request.POST or None)
	if form.is_valid():
		form.save(); messages.success(request, 'Enrollment created successfully.'); return redirect('enrollment_list')
	return render(request, 'students/form.html', {'form': form, 'title': 'Enroll student', 'back_url': 'enrollment_list'})


@login_required
def enrollment_delete(request, pk):
	enrollment = get_object_or_404(Enrollment, pk=pk)
	if request.method == 'POST':
		enrollment.delete(); messages.success(request, 'Enrollment removed successfully.'); return redirect('enrollment_list')
	return render(request, 'students/confirm_delete.html', {'object': enrollment, 'object_type': 'enrollment', 'cancel_url': 'enrollment_list'})
