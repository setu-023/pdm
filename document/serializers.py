from rest_framework import serializers

from .models import Document, Metadata, FileSharing

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Document
        fields='__all__'

class MetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model=Metadata
        fields='__all__'

class FileSharingSerializer(serializers.ModelSerializer):
    class Meta:
        model=FileSharing
        fields='__all__'