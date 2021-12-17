from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('list-courses/', views.listCourses, name='courses'),
    path('list-instructors/', views.listInstructors, name='instructors'),
    path('list-rooms/', views.listRooms, name='rooms'),
    path('list-departmetns/', views.listDepartments, name='departments'),
    path('list-timetables/', views.listTimetables, name='timetables'),
    path('add-course/', views.addCourse, name='addCourse'),
    path('add-instructor/', views.addInstructor, name='addInstructor'),
    path('add-room/', views.addRoom, name='addRoom'),
    path('add-department', views.addDepartment, name='addDepartment'),
    path('delete-course/<str:pk>', views.deleteCourse, name='deleteCourse'),
    path('delete-instructor/<str:pk>', views.deleteInstructor, name='deleteInstructor'),
    path('delete-room/<str:pk>', views.deleteRoom, name='deleteRoom'),
    path('delete-department/<str:pk>', views.deleteDepartment, name='deleteDepartment'),
    path('delete-timetable/<str:pk>', views.deleteTimetable, name='deleteTimetable'),
    path('udpate-course/<str:pk>', views.updateCourse, name='updateCourse'),
    path('update-instructor/<str:pk>', views.updateInstructor, name='updateInstructor'),
    path('update-department/<str:pk>', views.updateDepartment, name='updateDepartment'),
    path('udpate-room/<str:pk>', views.updateRoom, name='updateRoom'),
    path('update-timetable/<str:pk>', views.updateTimetable, name='updateTimetable'),
    path('generate-timetable', views.generateTimetableCSP, name='generateTimetable'),
    path('view-timetable/<str:pk>', views.viewTimetable, name='viewTimetable'),
]