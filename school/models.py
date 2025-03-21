from django.db import models
import os
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()


def school_picture_upload_to(instance, filename):
    name = str(instance.name).replace(" ", "")
    filename = filename.replace(" ", "")
    return os.path.join('school_picture', f"{name}_{filename}")


class School(models.Model):
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=255, blank=True,
                             null=True)
    district = models.CharField(max_length=255, blank=True,
                                null=True)
    place = models.CharField(max_length=255, blank=True,
                             null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)

    school_picture = models.ImageField(
        upload_to=school_picture_upload_to, blank=True)
    description = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['-id']
        verbose_name = "School"
        verbose_name_plural = "Schools"

    def __str__(self):
        return self.name


class SchoolPermission(models.Model):
    school = models.ForeignKey(
        School, on_delete=models.SET_NULL, null=True,)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,)
    can_crud = models.BooleanField(default=False)

    class Meta:
        unique_together = ('school', 'user')
        ordering = ['-id']
        verbose_name = "School Permission"
        verbose_name_plural = "School Permissions"

    def __str__(self):
        return f'{self.user.username} {self.school.name}'
