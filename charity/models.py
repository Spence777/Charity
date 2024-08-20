from django.db import models

# Create your models here.
class Cause(models.Model):
    image = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=255)
    description = models.TextField()
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    raised_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

    def progress_percentage(self):
        if self.goal_amount == 0:
            return 0
        return (self.raised_amount / self.goal_amount) * 100


class Donation(models.Model):
    cause = models.ForeignKey(Cause, on_delete=models.CASCADE)
    donor_name = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_anonymous = models.BooleanField(default=False)
    is_recurring = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.donor_name} - {self.amount}'