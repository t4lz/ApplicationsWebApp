from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.


class JobApplication(models.Model):
    # Status Choices:
    # -------------------------------------------------------------------------
    APPLICATION_SENT =      0
    INTERVIEW_SCHEDULED =   1
    WAITING_FOR_COMPANY =   2
    WAITING_FOR_CANDIDATE = 3
    APPLICATION_REJECTED =  4
    APPLICATION_ACCEPTED =  5
    HIRED =                 6
    # -------------------------------------------------------------------------
    COMPLETED_STATUSES = [APPLICATION_REJECTED, APPLICATION_ACCEPTED, HIRED]
    STATUS_CHOICES = (
        (
            (APPLICATION_SENT, 'Application Sent'),
            (INTERVIEW_SCHEDULED, 'Interview Scheduled'),
            (WAITING_FOR_COMPANY, 'Waiting for an Answer from the Company\'s Side'),
            (WAITING_FOR_CANDIDATE, 'Waiting for an Answer from the Candidate\'s Side'),
            (APPLICATION_REJECTED, 'Application Inactive - Rejected'),
            (APPLICATION_ACCEPTED, 'Application Completed - Accepted'),
            (HIRED, 'Hired'),
        )
    )

    company_name = models.CharField(max_length=128)
    position = models.CharField(max_length=128)
    result = models.BooleanField(default=True)
    process_start_date = models.DateField(auto_now_add=True)
    process_end_date = models.DateField(null=True)
    next_step = models.CharField(null=True, max_length=256)
    status = models.IntegerField(default=APPLICATION_SENT, choices=STATUS_CHOICES)
    last_changed = models.DateField(auto_now=True)

    def get_absolute_url(self):
        return reverse('appsapp:details', kwargs={'pk': self.pk})

    def __str__(self):
        return "{} // {}".format(self.company_name, self.position)

    def is_open(self):
        """
        Is the application process still going on?
        """
        return self.status not in [JobApplication.APPLICATION_REJECTED, JobApplication.APPLICATION_ACCEPTED,
                                   JobApplication.HIRED]

    def is_rejected(self):
        return self.status == JobApplication.APPLICATION_REJECTED


def make_path(instance, filename):
    """
    Get the path to save an uploaded file in: <company>/<position>/<file_type_name>/<original_filename>
    The path is relative to the MEDIA_ROOT set in applications/settings.py
    """
    company = slugify(instance.application.company_name)
    position = slugify(instance.application.position)
    file_type = slugify(instance.get_file_type_display())
    return "{}/{}/{}/{}".format(company, position, file_type, filename)


class ApplicationDocument(models.Model):
    # File Types:
    # -------------------------------------------------------------------------
    CV =                    0
    COVER_LETTER =          1
    TRANSCRIPT_OF_RECORDS = 2
    RANKING =               3
    OTHER =                 4
    # -------------------------------------------------------------------------
    FILE_TYPES = (
        (
            (CV, 'CV'),
            (COVER_LETTER, 'Cover Letter'),
            (TRANSCRIPT_OF_RECORDS, 'Transcript of Records'),
            (RANKING, 'Ranking Confirmation'),
            (OTHER, 'Other')
        )
    )
    file = models.FileField(upload_to=make_path)
    slug = models.SlugField(unique=True)
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE)
    file_type = models.IntegerField(choices=FILE_TYPES)
    file_name = models.CharField(max_length=256)

    def _get_unique_slug(self):
        """
        create a unique slug that will be used to download this file
        """
        slug = slugify("{}-{}-{}-{}".format(self.application.company_name, self.application.position,
                                            self.get_file_type_display(), self.file_name))
        num = 0
        while ApplicationDocument.objects.filter(slug=slug).exists():
            num +=1
            slug = slugify("{}-{}-{}-{}-{}".format(self.application.company_name, self.application.position,
                                                   self.get_file_type_display(), self.file_name, num))
        return slug

    def save(self, *args, **kwargs):
        """
        override save to create slug on saving the object.
        """
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


