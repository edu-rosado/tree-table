from rest_framework import serializers

from .models import TreeTable


class TreeTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreeTable
        fields = ('jsonRepr',)

    def to_representation(self, instance):
        # json in assigned on the go and it's not even saved
        # (the data is already 'relationaly' stored)
        instance.generateJson()
        ret = super().to_representation(instance)
        return ret


'''
from tree_table_app.serializers import TreeTableSerializer
from tree_table_app.models import *
t = TreeTable.objects.all()[0]
s = TreeTableSerializer(t)
s.data
'''
