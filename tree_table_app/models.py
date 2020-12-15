from django.core.exceptions import SuspiciousOperation
from django.db import models
from django.contrib.auth.models import User
from django.http.response import Http404


class Node(models.Model):
    parent = models.ForeignKey("self",
                               on_delete=models.CASCADE,
                               related_name="children",
                               null=True,
                               )
    text = models.CharField(max_length=2**15 - 1)  # 32k
    is_root = models.BooleanField(default=False)

    def generateJson(self):
        dic = {
            "id": self.id,
            "text": self.text,
            "children": [],
        }
        for child in self.children.all():
            dic["children"].append(child.generateJson())
        return dic

    def getLevel(self):
        return Node.auxGetLevel(self, 0)

    @staticmethod
    def auxGetLevel(node, lv):
        if node.is_root:
            return lv
        return Node.auxGetLevel(node.parent, lv+1)

    def __str__(self):
        return f"{self.text[:20]} <id:{self.id}>"

    def print(self, nIndent):
        s = "    "*nIndent + f"{self}"
        nIndent += 1
        for child in self.children.all():
            s += "\n" + child.print(nIndent)
        return s


class TreeTable(models.Model):
    name = models.CharField(max_length=254)
    root = models.OneToOneField(
        Node,
        on_delete=models.PROTECT,  # root should never be deleted unless the treetable is
        related_name="treeTable",
    )
    # json only to send the data, the actual data is stored in Nodes and the TreeTable
    jsonRepr = models.JSONField(null=True, default=None)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    depth = models.PositiveIntegerField(default=0)
    headers = models.JSONField(default=list)

    @classmethod
    def create(cls, name, owner):
        root = Node(is_root=True, text="<root>")
        root.save()
        try:
            owner_id = int(owner)
            instance = cls(name=name, root=root, owner_id=owner_id)
        except:
            instance = cls(name=name, root=root, owner=owner)
        return instance

    def generateJson(self):
        # Called in the serializer
        self.jsonRepr = self.root.generateJson()

    def addNode(self, text, parentNode):
        if type(parentNode) == int:
            try:
                parentNode = Node.objects.get(parentNode)
            except:
                raise Http404
        if parentNode.getLevel() == self.depth:
            self.depth += 1
            self.headers.append("")
            self.save()
        newNode = Node(text=text, parent=parentNode)
        newNode.save()

    def deleteNode(self, targetNode):
        if type(targetNode) == int:
            try:
                targetNode = Node.objects.get(targetNode)
            except:
                raise Http404
        if targetNode.is_root:
            raise SuspiciousOperation("You cannot delete the root node")
        if len(targetNode.parent.children) == 1 and targetNode.getLevel() == self.depth:
            self.depth -= 1
            self.headers.pop()
            self.save()
        targetNode.delete()

    def __str__(self):
        return f"{self.name}"

    def print(self):
        return self.root.print(0)
