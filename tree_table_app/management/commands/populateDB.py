from django.core.management.base import BaseCommand
from ...models import TreeTable, Node


class Command(BaseCommand):
    def handle(self, *args, **options):

        TreeTable.objects.all().delete()
        # Node.objects.all().delete()

        t1 = TreeTable.create(name="t1")
        t1.save()

        n1 = Node(parent=t1.root, text="n1")
        n1.save()

        n2 = Node(parent=t1.root, text="n2")
        n2.save()
        n21 = Node(parent=n2, text="n21")
        n21.save()
        n22 = Node(parent=n2, text="n22")
        n22.save()

        n3 = Node(parent=t1.root, text="n3")
        n3.save()
