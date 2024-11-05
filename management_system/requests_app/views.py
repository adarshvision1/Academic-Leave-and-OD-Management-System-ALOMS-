from django.shortcuts import render, redirect, get_object_or_404
from .models import ODRequest, LeaveIntimation
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import FileResponse, Http404
import os
from django.contrib.auth.decorators import user_passes_test

def is_tutor(user):
    return user.groups.filter(name='Tutor').exists()
def is_hod(user):
    return user.groups.filter(name='HoD').exists()
def is_student(user):
    return user.groups.filter(name='Student').exists()
def download_file(request, request_id):
    try:
        od_request = ODRequest.objects.get(id=request_id)  # Ensure we're fetching the ODRequest
        file_path = od_request.file.path if od_request.file else None
        if file_path and os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), as_attachment=True)
        else:
            raise Http404("File not found")
    except ODRequest.DoesNotExist:
        raise Http404("Request not found")

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirect based on user group
            if user.groups.filter(name='Student').exists():
                return redirect('student_dashboard')
            elif user.groups.filter(name='Tutor').exists():
                return redirect('tutor_dashboard')
            elif user.groups.filter(name='HoD').exists():
                return redirect('hod_dashboard')
            else:
                return redirect('login')
        else:
            error_message = "Invalid username or password."
            return render(request, 'login.html', {'error': error_message})
    
    return render(request, 'login.html')

@login_required
@user_passes_test(is_student)

def student_dashboard(request):
    od_requests = ODRequest.objects.filter(student=request.user)
    leave_intimations = LeaveIntimation.objects.filter(student=request.user)
    od_status = request.GET.get('od_status', None)
    leave_status = request.GET.get('leave_status', None)

    # Filter OD Requests
    if od_status:
        od_requests = ODRequest.objects.filter(status=od_status)
    else:
        od_requests = ODRequest.objects.all()

    # Filter Leave Intimations
    if leave_status:
        leave_intimations = LeaveIntimation.objects.filter(status=leave_status)
    else:
        leave_intimations = LeaveIntimation.objects.all()

    return render(request, 'student_dashboard.html', {
        'od_requests': od_requests,
        'leave_intimations': leave_intimations,
        'od_status': od_status,
        'leave_status': leave_status,
    })

@login_required
def apply_od(request):
    if request.method == 'POST':
        od_request = ODRequest(
            student=request.user,
            date=request.POST['date'],
            hours=request.POST['hours'],
            reason=request.POST['reason'],
            file=request.FILES['file']
        )
        od_request.save()
        return redirect('student_dashboard')
    return render(request, 'apply_od.html')

@login_required
def apply_leave(request):
    if request.method == 'POST':
        leave_intimation = LeaveIntimation(
            student=request.user,
            date=request.POST['date'],
            reason=request.POST['reason']
        )
        leave_intimation.save()
        return redirect('student_dashboard')
    return render(request, 'apply_leave.html')

@login_required
@user_passes_test(is_tutor)
def tutor_dashboard(request):
    # Fetching all OD requests and leave intimations for the tutor dashboard
    od_requests = ODRequest.objects.all()  # Fetch all OD requests
    leave_intimations = LeaveIntimation.objects.all()  # Fetch all leave intimations
    return render(request, 'tutor_dashboard.html', {'od_requests': od_requests, 'leave_intimations': leave_intimations})


@login_required
def approve_od(request, od_id):
    od_request = get_object_or_404(ODRequest, id=od_id)
    od_request.status = 'Tutor Approved'
    od_request.save()
    return redirect('tutor_dashboard')  # Redirect back to the tutor dashboard to show updated requests

@login_required
def deny_od(request, od_id):
    od_request = get_object_or_404(ODRequest, id=od_id)
    od_request.status = 'Denied'
    od_request.save()
    return redirect('tutor_dashboard')  # Redirect back to the tutor dashboard

@login_required
def approve_leave(request, leave_id):
    leave_intimation = get_object_or_404(LeaveIntimation, id=leave_id)
    leave_intimation.status = 'Tutor Approved'
    leave_intimation.save()
    return redirect('tutor_dashboard')  # Redirect back to the tutor dashboard

@login_required
def deny_leave(request, leave_id):
    leave_intimation = get_object_or_404(LeaveIntimation, id=leave_id)
    leave_intimation.status = 'Denied'
    leave_intimation.save()
    return redirect('tutor_dashboard')  # Redirect back to the tutor dashboard

@login_required
@user_passes_test(is_hod)

def hod_dashboard(request):
    # Fetching all requests for the HoD dashboard
    od_requests = ODRequest.objects.all()
    leave_intimations = LeaveIntimation.objects.all()
    return render(request, 'hod_dashboard.html', {'od_requests': od_requests, 'leave_intimations': leave_intimations})

@login_required
def hod_approve_od(request, od_id):
    od_request = get_object_or_404(ODRequest, id=od_id)
    od_request.status = 'HoD Approved'
    od_request.save()
    return redirect('hod_dashboard')  # Redirect back to the HoD dashboard

@login_required
def hod_deny_od(request, od_id):
    od_request = get_object_or_404(ODRequest, id=od_id)
    od_request.status = 'Denied'
    od_request.save()
    return redirect('hod_dashboard')  # Redirect back to the HoD dashboard

@login_required
def hod_approve_leave(request, leave_id):
    leave_intimation = get_object_or_404(LeaveIntimation, id=leave_id)
    leave_intimation.status = 'HoD Approved'
    leave_intimation.save()
    return redirect('hod_dashboard')  # Redirect back to the HoD dashboard

@login_required
def hod_deny_leave(request, leave_id):
    leave_intimation = get_object_or_404(LeaveIntimation, id=leave_id)
    leave_intimation.status = 'Denied'
    leave_intimation.save()
    return redirect('hod_dashboard')  # Redirect back to the HoD dashboard
