from datetime import date, timedelta

from django.core.management.base import BaseCommand

from students.models import Course, Department, Enrollment, Student


class Command(BaseCommand):
    help = 'Create realistic demo departments, courses, students, and enrollments.'

    def handle(self, *args, **options):
        department_names = ['Computer Science', 'Information Technology', 'Mechanical Engineering', 'Civil Engineering', 'Electronics']
        departments = {name: Department.objects.get_or_create(name=name, defaults={'description': f'{name} academic department.'})[0] for name in department_names}
        course_data = [('Introduction to Programming', 'CS101', 'Computer Science', 4), ('Data Structures', 'CS201', 'Computer Science', 4), ('Database Systems', 'CS301', 'Computer Science', 3), ('Web Development', 'IT201', 'Information Technology', 3), ('Network Fundamentals', 'IT202', 'Information Technology', 3), ('Thermodynamics', 'ME201', 'Mechanical Engineering', 4), ('Fluid Mechanics', 'ME301', 'Mechanical Engineering', 3), ('Machine Design', 'ME302', 'Mechanical Engineering', 3), ('Structural Analysis', 'CE201', 'Civil Engineering', 4), ('Surveying', 'CE202', 'Civil Engineering', 3), ('Environmental Engineering', 'CE301', 'Civil Engineering', 3), ('Digital Electronics', 'EC201', 'Electronics', 4), ('Signals and Systems', 'EC301', 'Electronics', 3), ('Microprocessors', 'EC302', 'Electronics', 3), ('Embedded Systems', 'EC303', 'Electronics', 4)]
        courses = [Course.objects.get_or_create(code=code, defaults={'name': name, 'department': departments[department], 'credits': credits, 'description': f'{name} course.'})[0] for name, code, department, credits in course_data]
        first_names = ['Aarav', 'Diya', 'Kabir', 'Meera', 'Arjun', 'Anaya', 'Rohan', 'Ishita', 'Vivaan', 'Saanvi', 'Aditya', 'Kiara', 'Reyansh', 'Nisha', 'Ayaan', 'Tara', 'Dev', 'Mira', 'Neil', 'Riya', 'Karan', 'Aisha', 'Om', 'Sara', 'Yash', 'Ira', 'Ritvik', 'Navya', 'Veer', 'Myra']
        last_names = ['Sharma', 'Patel', 'Shah', 'Iyer', 'Reddy', 'Kapoor', 'Singh', 'Mehta', 'Nair', 'Joshi']
        department_list = list(departments.values())
        students = []
        for index, first_name in enumerate(first_names, start=1):
            students.append(Student.objects.get_or_create(student_id=f'STU{index:03d}', defaults={'first_name': first_name, 'last_name': last_names[(index - 1) % len(last_names)], 'email': f'student{index}@campus.example', 'phone': f'+91 90000 {index:05d}', 'gender': ['M', 'F', 'O'][(index - 1) % 3], 'department': department_list[(index - 1) % len(department_list)], 'enrollment_date': date.today() - timedelta(days=index * 4)})[0])
        for index, student in enumerate(students):
            Enrollment.objects.get_or_create(student=student, course=courses[index % len(courses)])
            Enrollment.objects.get_or_create(student=student, course=courses[(index + 3) % len(courses)])
        self.stdout.write(self.style.SUCCESS(f'Seeded {len(departments)} departments, {len(courses)} courses, {len(students)} students, and demo enrollments.'))