from django.db import models


class Node(models.Model):
    parent = models.ForeignKey("self",
                               on_delete=models.CASCADE,
                               related_name="children",
                               null=True,
                               )
    text = models.CharField(max_length=2**15 - 1)  # 32k
    is_root = models.BooleanField(default=False)

    def findById(self, nodeId):
        if self.id == nodeId:
            return self
        for child in self.children.all():
            res = child.findById(nodeId)
            if res is not None:
                return res
        return None

    def generateJson(self):
        dic = {
            "id": self.id,
            "text": self.text,
            "children": [],
        }
        for child in self.children.all():
            dic["children"].append(child.generateJson())
        return dic

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

    @classmethod
    def create(cls, name):
        root = Node(is_root=True, text="<root>")
        root.save()
        instance = cls(name=name, root=root)
        return instance

    def findById(self, nodeId):
        return self.root.findById(nodeId)

    def generateJson(self):
        # Called in the serializer
        self.jsonRepr = self.root.generateJson()

    def __str__(self):
        return f"{self.name}"

    def print(self):
        return self.root.print(0)
