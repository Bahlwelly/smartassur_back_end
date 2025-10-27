from django.core.mail import send_mail
from django.utils import timezone
from contract.models import Contract
from django.conf import settings


def send_expiration_email () :
    expired_contracts = Contract.objects.filter(end_date__lte=timezone.now().date(), notified=False)
        
    for contract in expired_contracts :
        try :
            send_mail(
                f"Your contract has expired",
                f"Hello, your contract with {contract.product.company.name} has expired",
                settings.DEFAULT_FROM_EMAIL,
                [contract.client.email]
            )

            contract.notified = True
            contract.status = 'expired'
            contract.save()
            print(f"Email was sent to {contract.client.email}")
            

        except Exception as e :
            print(f"Faild to send email to {contract.client.email} : \n{e}")