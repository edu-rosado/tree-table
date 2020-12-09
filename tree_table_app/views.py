from django.shortcuts import render
from django.http import Http404
from django.core.exceptions import SuspiciousOperation

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import TableTree, Node, TreeTable
from .serializers import TreeTableSerializer


class TableTreeList(APIView):
    def get(self, request):
        tableTrees = TableTree.objects.filter(owner=request.user)
        serializer = TreeTableSerializer(tableTrees, many=True)
        return Response(serializer.data)

    def post(self, request):
        TableTree.create(request.body["name"], request.body["owner"]).save()


class TableTreeDetail(APIView):
    def get_object(self, id):
        try:
            return TreeTable.objects.get(id=id)
        except TableTree.DoesNotExist:
            raise Http404

    def get(self, request, id):
        tableTree = self.get_object(id)
        serializer = TreeTableSerializer(tableTree)
        return Response(serializer.data)

    def put(self, request, id):
        tableTree = self.get_object(id)
        for operation in request.body:
            opKey = operation["opKey"]
            node = tableTree.findById(operation["nodeId"])
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
        tableTree = self.get_object(id)
        tableTree.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
