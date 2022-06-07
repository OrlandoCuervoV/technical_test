from django.db import models

STATUS_CHOICES = (
    ("active", ("active")),
    ("inactive", ("inactive"))
)


class Category(models.Model):
    code = models.CharField(max_length=10, blank=False, null=False)
    title = models.CharField(max_length=10, blank=False, null=False)
    description = models.TextField(max_length=500, blank=False, null=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', blank=False, null=False)
    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    deleted_at = models.DateField(null=True, blank=True)
    tree = TreeManager()