from django.db import models

# Create your models here.
class Poll(models.Model):
    question = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.question

class Option(models.Model):
    poll = models.ForeignKey(Poll, related_name='options', on_delete=models.CASCADE)
    option_text = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.option_text} ({self.poll.question})"

class Vote(models.Model):
    option = models.ForeignKey(Option, related_name='votes', on_delete=models.CASCADE)
    voter_identifier = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class Vote(models.Model):
    option = models.ForeignKey(Option, related_name='votes', on_delete=models.CASCADE)
    voter_identifier = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['voter_identifier', 'option'],  
                name='unique_vote_per_poll'
            )
        ]

    def __str__(self):
        return f"Vote for {self.option.option_text} by {self.voter_identifier}"