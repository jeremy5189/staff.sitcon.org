from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from users.models import *
from users.utils import validate_email

def profile(request, id):
	u = get_object_or_404(User, pk=id)
	return render(request, 'users_profile.html', {
		'u': u,
	})

def edit_profile(request, user):
	errors = []
	status = ''

	if request.POST.get('submit'):
		profile = None
		try:
			profile = user.profile
		except UserProfile.DoesNotExist:
			profile = UserProfile(user=user)

		if request.user.has_perm('auth.change_user'):
			username = request.POST.get('username')
			if username != user.username:
				if username:
					if User.objects.filter(username=username).count() < 1:
						user.username = username
					else:
						errors += ['username', 'username_already_taken']
				else:
					errors += ['username', 'invalid_username']

			profile.title = request.POST.get('title')
		
		user.first_name = request.POST.get('first_name')
		user.last_name = request.POST.get('last_name')

		email = request.POST.get('email', '')
		if email != user.email:
			if validate_email(email):
				if User.objects.filter(email=email).count() < 1:
					user.email = email
				else:
					errors += ['email', 'email_already_taken']
			else:
				errors += ['email', 'invalid_email']

		profile.display_name = request.POST.get('display_name')
		profile.school = request.POST.get('school')
		profile.grade = request.POST.get('grade')
		profile.phone = request.POST.get('phone')
		profile.comment = request.POST.get('comment')

		if len(errors) < 1:
			user.save()
			profile.save()
			status = 'success'
		else:
			status = 'error'

	return render(request, 'users_edit_profile.html', {
		'u': user,
		'errors': errors,
		'status': status,
	})
