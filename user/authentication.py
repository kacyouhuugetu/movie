from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

from django.db.models import Q

class EmailAuthBackend(ModelBackend):
	def authenticate(self, request, username=None, password=None):
		try:
			user = User.objects.get(Q(email=username))
			if user.check_password(password):
				return user
			return None
		except User.DoesNotExist:
			return None