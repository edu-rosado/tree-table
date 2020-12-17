from django.core.management.base import BaseCommand
from ...models import TreeTable, Node
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):

        TreeTable.objects.all().delete()

        admin = User.objects.get(username="admin")
        t1 = TreeTable.create(name="t1", owner=admin)
        t1.save()

        n1_id = t1.addNode(text="n1", parentNode=t1.root)
        n11_id = t1.addNode(text="n11", parentNode=n1_id)
        n111_id = t1.addNode(text="n111", parentNode=n11_id)
        n112_id = t1.addNode(text="n112", parentNode=n11_id)

        n2_id = t1.addNode(text="n2", parentNode=t1.root)

        n3_id = t1.addNode(text="n3", parentNode=t1.root)
        n31_id = t1.addNode(text="n31", parentNode=n3_id)
        n32_id = t1.addNode(text="n32", parentNode=n3_id)

        t2 = TreeTable.create(name="t2", owner=admin)
        t2.save()
        t2_n1 = t2.addNode(text="t2_n1", parentNode=t2.root)
