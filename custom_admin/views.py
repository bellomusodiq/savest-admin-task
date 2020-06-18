from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import DetailView
from .forms import SendEmailForm
from django.core.paginator import Paginator
import datetime
from datetime import timedelta
from django.utils import timezone
# Create your views here.


class CustomAdmin(View):
    """
    endpoint: /admin/
    This class is used to get and filter all/filtered user to the custom_admin.html template
    """

    def get(self, request):
        all_users = User.objects.all().order_by('-date_joined')
        all_staffs = all_users.filter(is_staff=True)
        all_active_users = all_users.filter(is_active=True)
        all_inactive_users = all_users.filter(is_active=False)

        user_page = 1
        if request.GET.get('user_page'):
            user_page = int(request.GET.get('user_page'))
            print(user_page)
        staffs_page = 1
        if request.GET.get('staffs_page'):
            staffs_page = int(request.GET.get('staffs_page'))
        active_users_page = 1
        if request.GET.get('active_users_page'):
            active_users_page = int(request.GET.get('active_users_page'))
        inactive_users_page = 1
        if request.GET.get('inactive_users_page'):
            inactive_users_page = int(request.GET.get('inactive_users_page'))

        user_paginator = Paginator(all_users, 10)
        staff_paginator = Paginator(all_staffs, 10)
        active_users_paginator = Paginator(all_active_users, 10)
        inactive_users_paginator = Paginator(all_inactive_users, 10)

        all_users = {
            'total_count': user_paginator.count,
            'num_pages': user_paginator.num_pages,
            'page_range': user_paginator.page_range,
            'data': user_paginator.page(user_page).object_list,
            'has_next': user_paginator.page(user_page).has_next(),
            'has_previous': user_paginator.page(user_page).has_previous(),
            'current_page': user_page
        }

        all_staffs = {
            'total_count': staff_paginator.count,
            'num_pages': staff_paginator.num_pages,
            'page_range': staff_paginator.page_range,
            'data': staff_paginator.page(staffs_page).object_list,
            'has_next': staff_paginator.page(staffs_page).has_next(),
            'has_previous': staff_paginator.page(staffs_page).has_previous(),
            'current_page': staffs_page
        }

        all_active_users = {
            'total_count': active_users_paginator.count,
            'num_pages': active_users_paginator.num_pages,
            'page_range': active_users_paginator.page_range,
            'data': active_users_paginator.page(active_users_page).object_list,
            'has_next': active_users_paginator.page(active_users_page).has_next(),
            'has_previous': active_users_paginator.page(active_users_page).has_previous(),
            'current_page': active_users_page
        }

        all_inactive_users = {
            'total_count': inactive_users_paginator.count,
            'num_pages': inactive_users_paginator.num_pages,
            'page_range': inactive_users_paginator.page_range,
            'data': inactive_users_paginator.page(inactive_users_page).object_list,
            'has_next': inactive_users_paginator.page(inactive_users_page).has_next(),
            'has_previous': inactive_users_paginator.page(inactive_users_page).has_previous(),
            'current_page': inactive_users_page
        }

        users = {
            '24hrs_users': User.objects.filter(date_joined__gte=timezone.now() - timedelta(days=1)).count(),
            'past_week': User.objects.filter(date_joined__gte=timezone.now() - timedelta(weeks=1)).count(),
            'past_month': User.objects.filter(date_joined__gte=timezone.now() - timedelta(weeks=4)).count(),
            'all_users': all_users,
            'all_staffs': all_staffs,
            'all_active_users': all_active_users,
            'all_inactive_users': all_inactive_users,
        }
        return render(request, 'custom_admin.html', users)


class CustomAdminDetail(DetailView):
    template_name = 'custom_admin_detail.html'
    model = User


class SendEmail(View):

    def get(self, request):
        print(request)
        return render(request, 'compose_email.html', {})

    def post(self, request):
        user = User.objects.filter(is_active=True)
        form = SendEmailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/custom_admin/')
        return render(request, 'compose_email.html', {'user': user, 'errors': form.errors})


class ActivateOrDisableAccount(View):

    def get(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        status = request.GET.get('status')
        if status == 'true':
            user.is_active = True
        else:
            user.is_active = False
        user.save()
        return redirect('/custom_admin/')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')
