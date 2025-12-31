from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()


class Exam(models.Model):
    """
    Represents an exam/assessment with metadata including timing and course information.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    # Required fields
    title = models.CharField(max_length=255, help_text="Name/title of the exam")
    duration = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Time limit for completing the exam in minutes"
    )
    course = models.CharField(max_length=255, help_text="Associated course or subject")
    
    # Metadata fields
    description = models.TextField(blank=True, null=True, help_text="Exam description")
    total_marks = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        help_text="Total marks for the exam"
    )
    passing_score = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        help_text="Minimum score required to pass"
    )
    start_datetime = models.DateTimeField(
        blank=True, 
        null=True, 
        help_text="When the exam becomes available"
    )
    end_datetime = models.DateTimeField(
        blank=True, 
        null=True, 
        help_text="When the exam closes"
    )
    instructions = models.TextField(
        blank=True, 
        null=True, 
        help_text="Instructions for students"
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='draft',
        help_text="Current status of the exam"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'start_datetime']),
            models.Index(fields=['course']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.title


class Question(models.Model):
    """
    Represents a question within an exam.
    """
    QUESTION_TYPE_CHOICES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('short_answer', 'Short Answer'),
        ('essay', 'Essay'),
        ('fill_blank', 'Fill in the Blank'),
    ]

    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    # Required fields
    exam = models.ForeignKey(
        Exam, 
        on_delete=models.CASCADE, 
        related_name='questions',
        help_text="The exam this question belongs to"
    )
    question_text = models.TextField(help_text="The actual question content")
    question_type = models.CharField(
        max_length=20, 
        choices=QUESTION_TYPE_CHOICES,
        help_text="Type of question"
    )
    expected_answer = models.JSONField(
        help_text="The correct answer or answer key (format depends on question type)"
    )
    marks = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        help_text="Point value for the question"
    )
    
    # Optional fields
    order = models.IntegerField(
        blank=True, 
        null=True,
        help_text="Question sequence number within the exam"
    )
    
    # Metadata fields
    difficulty_level = models.CharField(
        max_length=20, 
        choices=DIFFICULTY_CHOICES, 
        blank=True, 
        null=True,
        help_text="Difficulty level of the question"
    )
    topic = models.CharField(
        max_length=255, 
        blank=True, 
        null=True,
        help_text="Topic or category"
    )
    grading_criteria = models.TextField(
        blank=True, 
        null=True,
        help_text="Grading criteria for essay questions"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['exam', 'order', 'id']
        indexes = [
            models.Index(fields=['exam', 'order']),
            models.Index(fields=['question_type']),
        ]

    def __str__(self):
        return f"{self.exam.title} - Question {self.order or self.id}"


class Answer(models.Model):
    """
    Represents a student's answer to a specific question in a submission.
    """
    submission = models.ForeignKey(
        'Submission',
        on_delete=models.CASCADE,
        related_name='answers',
        help_text="The submission this answer belongs to"
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='student_answers',
        help_text="The question being answered"
    )
    student_answer = models.JSONField(
        help_text="The student's answer (format depends on question type)"
    )
    marks_awarded = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text="Marks awarded for this answer"
    )
    feedback = models.TextField(
        blank=True,
        null=True,
        help_text="Feedback for this specific answer"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['submission', 'question__order', 'question__id']
        indexes = [
            models.Index(fields=['submission', 'question']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['submission', 'question'],
                name='unique_submission_question'
            ),
        ]

    def __str__(self):
        return f"{self.submission.student.username} - {self.question.question_text[:50]}"


class Submission(models.Model):
    """
    Represents a student's exam submission with grading status and feedback.
    """
    GRADING_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    # Required fields
    student = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='submissions',
        help_text="The student who submitted this exam"
    )
    exam = models.ForeignKey(
        Exam, 
        on_delete=models.CASCADE, 
        related_name='submissions',
        help_text="The exam being submitted"
    )
    # Answers are now stored in the separate Answer model with reverse relation 'answers'
    start_time = models.DateTimeField(
        help_text="When the student began the exam"
    )
    submit_time = models.DateTimeField(
        help_text="When the student submitted the exam"
    )
    
    # Grading fields
    grade = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        blank=True, 
        null=True,
        validators=[MinValueValidator(0)],
        help_text="Final score received"
    )
    grading_status = models.CharField(
        max_length=20, 
        choices=GRADING_STATUS_CHOICES, 
        default='pending',
        help_text="Status of the grading process"
    )
    grading_feedback = models.JSONField(
        blank=True, 
        null=True,
        help_text="Detailed feedback on answers"
    )
    
    # Calculated field
    time_taken = models.IntegerField(
        blank=True, 
        null=True,
        help_text="Duration the student took to complete in seconds"
    )
    
    # Metadata fields
    ip_address = models.GenericIPAddressField(
        blank=True, 
        null=True,
        help_text="IP address from which submission was made"
    )
    user_agent = models.TextField(
        blank=True, 
        null=True,
        help_text="Browser/device information"
    )
    attempt_number = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text="Attempt number if retakes are allowed"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-submit_time']
        indexes = [
            models.Index(fields=['student', 'exam']),
            models.Index(fields=['student', '-submit_time']),
            models.Index(fields=['grading_status']),
            models.Index(fields=['exam', 'grading_status']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'exam', 'attempt_number'],
                name='unique_student_exam_attempt'
            ),
        ]

    def __str__(self):
        return f"{self.student.username} - {self.exam.title} (Attempt {self.attempt_number})"
    
    def save(self, *args, **kwargs):
        """
        Override save to calculate time_taken if not provided.
        """
        if self.start_time and self.submit_time and not self.time_taken:
            time_diff = self.submit_time - self.start_time
            self.time_taken = int(time_diff.total_seconds())
        super().save(*args, **kwargs)
