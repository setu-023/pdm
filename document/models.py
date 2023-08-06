from sys import maxsize
from django.db import models
from django.core.exceptions import ValidationError
import os

from account.models import User

class Type(models.Model):
    DOCUMENT_TYPE = (
        ("txt","txt"),
        ("pdf","pdf"),
        ("docx","docx"),
        ("jpg","jpg"),
    )
    document_type = models.CharField(max_length=25, choices=DOCUMENT_TYPE)
    file_size = models.IntegerField()

    is_active = models.BooleanField(default=True,null=True, blank=True )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


# def validate_file(file):

#     get_extention=(os.path.splitext(file.name)[1])
#     get_extention=(get_extention.split('.'))[1]
#     get_file_size = Type.objects.get(document_type=get_extention).file_size
#     print(get_file_size)

#     # validate file size
#     # 10 MB = 10485760 bytes. 
#     if file.size > get_file_size:
#         print('not allow')
#         raise ValidationError('not allow')
#     else:
#         print("allow")
#     return True


class Document(models.Model):

    uploaded_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, related_name="document", on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/')

    ##meta data
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    
    is_active = models.BooleanField(default=True,null=True, blank=True )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


    def save(self, *args, **kwargs):
        get_document_type_instance = Type.objects.get(id=self.type.id)
        get_document_type = get_document_type_instance.document_type

        get_extention=(os.path.splitext(self.file.name)[1])
        get_extention=(get_extention.split('.'))[1]
        
        # validate file extention
        if get_document_type!=get_extention:
            print('file are not same')
            raise ValueError ('not allow')
        else:
            # validate file size
            if self.file.size > get_document_type_instance.file_size:
                print('file size in not okay')
                raise ValueError ('file size is too big')
            else:
                print('files are same and under in size')
                super(Document, self).save(*args, **kwargs)


    
