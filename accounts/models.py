from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.db.models.fields.files import ImageField
from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

email_suffix = "@" + settings.INTERNAL_DOMAIN

# Create your models here.
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=255, blank=True)
    image = ImageField(upload_to="profile_pics", blank=True, null=True)
    image_url = models.TextField(blank=True, null=True)
    timezone = models.CharField(max_length=50, default="US/Pacific")
    title = models.CharField(max_length=255, blank=True)

    def is_new_user(self):
        return self.date_joined > timezone.now() - timedelta(hours=1)

    def is_employee(self):
        return (
            email_suffix in self.email or self.groups.filter(name="employee").exists()
        )

    def do_employee_check(self):
        if self.is_employee() and self.groups.count() == 0:
            logger.info(f"adding {self.email} to employee group")
            emp_group, _ = Group.objects.get_or_create(name="employee")
            self.groups.add(emp_group)
            self.save()

    def setup_profile_pic(self):
        if self.socialaccount_set.count() > 0 and self.image_url is None:
            socialaccount = self.socialaccount_set.first()

            # this section is untested
            if socialaccount.provider == "twitter":
                name = socialaccount.extra_data["name"]
                self.first_name = name.split()[0]
                self.last_name = name.split()[1]

            # this section is untested
            if socialaccount.provider == "facebook":
                f_name = socialaccount.extra_data["first_name"]
                l_name = socialaccount.extra_data["last_name"]
                if f_name:
                    self.first_name = f_name
                if l_name:
                    self.last_name = l_name

                # verified = sociallogin.account.extra_data['verified']
                picture_url = (
                    "http://graph.facebook.com/{0}/picture?width={1}&height={1}".format(
                        socialaccount.uid, preferred_avatar_size_pixels
                    )
                )

            # this section IS tested
            if socialaccount.provider == "google":
                f_name = socialaccount.extra_data["given_name"]
                l_name = socialaccount.extra_data["family_name"]
                if f_name:
                    self.first_name = f_name
                if l_name:
                    self.last_name = l_name
                # verified = sociallogin.account.extra_data['verified_email']
                picture_url = socialaccount.get_avatar_url()

            self.image_url = picture_url
            self.save()
