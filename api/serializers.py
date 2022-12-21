from rest_framework import serializers






class VerifyPaymentSerializer(serializers.Serializer):
    reference = serializers.CharField(allow_blank=True)
    type = serializers.CharField(allow_blank=True)
