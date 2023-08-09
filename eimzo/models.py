from django.db import models
from django.utils.translation import gettext as _


class Key(models.Model):
    id = models.AutoField(primary_key=True)
    
    serial_number = models.CharField(
        verbose_name=_("Serial number"),
        max_length=8,
        unique=True, null=False, blank=False,
        help_text=_("Certificate serial number"),
    )
    
    class KeyType(models.IntegerChoices):
        jismoniy = (1, 'jismoniy')
        yuridik = (2, 'yuridik')
    
    type = models.SmallIntegerField(
        verbose_name=_("Key type"),
        null=False, blank=False,
        choices=KeyType.choices,
        help_text=_("Key type: 1-jismoniy, 2-yuridik")
    )
    
    file = models.FileField(
        verbose_name=_("Certificate file"),
        unique=True,
        null=False, blank=False,
        help_text=_("Certificate file")
    )
    
    password = models.CharField(
        verbose_name=_("Password"),
        max_length=15,
        null=False, blank=False,
        help_text=_("Password of certificate"),
    )
    
    name = models.CharField(
        verbose_name=_("Name"),
        null=False, blank=False,
        max_length=100,
        help_text=_("Name of the certificate holder")
    )
    
    surname = models.CharField(
        verbose_name=_("Surname"),
        null=False, blank=False,
        max_length=100,
        help_text=_("Surname of the certificate holder")
    )
    
    full_name = models.CharField(
        verbose_name=_("Full name"),
        null=False, blank=False,
        max_length=255,
        help_text=_("Full name of the certificate holder")
    )
    
    jshshir = models.PositiveIntegerField(
        verbose_name=_("JSHSHIR"),
        null=False, blank=False,
        help_text=_("Personal Identification Number of an Individual")
    )
    
    valid_from = models.DateTimeField(
        verbose_name=_("Valid from datetime"),
        null=False, blank=False,
        help_text=_("Date of validity of the certificate")
    )
    
    valid_to = models.DateTimeField(
        verbose_name=_("Valid to datetime"),
        null=False, blank=False,
        help_text=_("Until what date is the certificate valid")
    )
    
    location = models.CharField(
        verbose_name=_("Location"),
        max_length=100,
        null=False, blank=False,
        help_text=_("Location of certificate holder"),
    )
    
    city = models.CharField(
        verbose_name=_("City"),
        max_length=100,
        null=False, blank=False,
        help_text=_("City of certificate holder"),
    )
    
    country = models.CharField(
        verbose_name=_("Country"),
        max_length=100,
        null=False, blank=False,
        help_text=_("Country of certificate holder"),
    )
    
    stir = models.PositiveIntegerField(
        verbose_name=_("STIR"),
        null=True, blank=True,
        help_text=_("Taxpayer identification number"),
    )
    
    organization = models.CharField(
        verbose_name=_("Organization"),
        null=True, blank=True,
        max_length=150,
        help_text=_("Organization name"),
    )
    
    employee_type = models.CharField(
        verbose_name=_("Employee type"),
        null=True, blank=True,
        max_length=50,
        help_text=_("Employee type: Director/Manager/worker..."),
    )
    
    ou = models.CharField(
        verbose_name=_("OU"),
        null=True, blank=True,
        max_length=100,
        help_text=_("higher organization"),
    )
    
    business_category = models.CharField(
        verbose_name=_("Business category"),
        null=True, blank=True,
        max_length=100,
        help_text=_("Business category"),
    )
    
    uid = models.PositiveIntegerField(
        verbose_name=_("UID"),
        null=True, blank=True,
        help_text=_("Unique ID"),
    )
    