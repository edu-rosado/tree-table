from django.http.response import JsonResponse
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
        """
        It accepts a list of operations to perform on the nodes of the tree
        It is not transactional, so if a operation fails, the previous ops take effect
            regardless and the remaining ops  will not execute
        By sending a list of operations instead of sending the whole tree or sending
            many individual operations, the api should scale better
        """
        treeTable = self.get_object(id)
        for operation in request.data:
            opKey = operation["op_key"]
            try:
                node = Node.objects.get(operation["node_id"])
            except:
                raise Http404
            if opKey == "change_text":
                if node.is_root:
                    raise SuspiciousOperation(
                        "You cannot change the state of a root node")
                node.text = operation["text"]
                node.save()
            elif opKey == "add_child":
                new_node_id = treeTable.addNode(
                    text=operation["text"], parentNode=node)
                return JsonResponse({"id": new_node_id})
            elif opKey == "delete":
                treeTable.deleteNode(targetNode=node)
                if node.is_root:
                    raise SuspiciousOperation("You cannot delete a root node")
                node.delete()
            else:
                raise SuspiciousOperation("Invalid request")
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, id):
        treeTable = self.get_object(id)
        treeTable.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
