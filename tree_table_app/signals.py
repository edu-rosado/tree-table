
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Node, TreeTable


@receiver(post_delete, sender=TreeTable)
def deleteRoot(sender, instance, using, **kwargs):
    print(f"post deleting {instance}")
    instance.root.delete()


@receiver(post_delete, sender=Node)
def deleteChildren(sender, instance, using, **kwargs):
    print(f"post deleting {instance}")
    for child in instance.children.all():
        print(f"\tdeleting {child}")
        child.delete()
