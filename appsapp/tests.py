from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import ApplicationDocument, JobApplication


class JobApplModelTests(TestCase):

    def test_status_choices_codes_are_unique(self):
        """
        Make sure no statuses have the same code
        """
        codes = [tup[0] for tup in JobApplication.STATUS_CHOICES]
        self.assertEqual(len(codes), len(set(codes)), "Job application status codes are not all unique!")


def create_jobappl(company='ACME Corporation', position='Django and AI Engineer'):
    """
    Create a JobApplication object (not saved)
    Mostly using for the default values.
    """
    return JobApplication(company_name=company, position=position)


def create_doc_obj(application, file_type, name='Document1.txt'):
    """
    create an ApplicationDocument object (NOT SAVED)
    """
    doc = ApplicationDocument()
    doc.application = application
    doc.file_name = name
    doc.file = SimpleUploadedFile(name, b'mock content')
    doc.file_type = file_type
    return doc


class ApplDocModelTests(TestCase):

    def test_file_type_choices_codes_are_unique(self):
        """
        Make sure no file types have the same code
        """
        codes = [tup[0] for tup in ApplicationDocument.FILE_TYPES]
        self.assertEqual(len(codes), len(set(codes)), "Document file type codes are not all unique!")

    def test_upload_same_file(self):
        """
        Upload the a file to the same application with the same role (file type) and the same name and see that it there
        are no errors and the file does not override the old file, and that both have unique slugs.
        """
        jobappl = create_jobappl()
        jobappl.save()
        doc1 = create_doc_obj(application=jobappl, file_type=ApplicationDocument.CV)
        doc1.save()
        doc2 = create_doc_obj(application=jobappl, file_type=ApplicationDocument.CV)
        doc2.save()
        count = ApplicationDocument.objects.count()
        self.assertEqual(count, 2, "Added 2 identical files, expected 2 files in DB, found {}.".format(count))
        self.assertNotEqual(doc1.slug, doc2.slug, "2 (identical) files got the same slug")
