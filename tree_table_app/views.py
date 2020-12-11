from django.shortcuts import render
from django.http import Http404
from django.core.exceptions import SuspiciousOperation

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import TreeTable, Node
from .serializers import TreeTableSerializer


class TreeTableList(APIView):
    def get(self, request):
        treeTables = TreeTable.objects.filter(owner=request.user)
        serializer = TreeTableSerializer(treeTables, many=True)
        return Response(serializer.data)

    def post(self, request):
        # TODO: Validate the body data
        newT = TreeTable.create(
            name=request.data["name"], owner=request.data["owner_id"])
        newT.save()
        serializer = TreeTableSerializer(newT)
        return Response(serializer.data)


class TreeTableDetail(APIView):
    def get_object(self, id):
        try:
            return TreeTable.objects.get(id=id)
        except TreeTable.DoesNotExist:
            raise Http404

    def get(self, request, id):
        treeTable = self.get_object(id)
        serializer = TreeTableSerializer(treeTable)
        return Response(serializer.data)

    def put(self, request, id):
        treeTable = self.get_object(id)
        for operation in request.body:
            opKey = operation["opKey"]
            node = treeTable.findById(operation["nodeId"])
            if opKey == "changeText":
                node.text = operation["text"]
                node.save()
            elif opKey == "addChild":
                Node(parent=node, text=operation["text"]).save()
            elif opKey == "delete":
                node.delete()
            else:
                raise SuspiciousOperation("Invalid request")
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, id):
        treeTable = self.get_object(id)
        treeTable.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
