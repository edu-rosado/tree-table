from rest_framework import serializers

from .models import TreeTable


class TreeTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreeTable
        fields = ('id', 'jsonRepr', 'name', 'headers', 'depth')

    def to_representation(self, instance):
        # json in assigned on the go and it's not even saved
        # (the data is already 'relationaly' stored)
        instance.generateJson()
        return super().to_representation(instance)
