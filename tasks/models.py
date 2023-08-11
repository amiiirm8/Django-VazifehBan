from django.db import models
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _


class Task(models.Model):
    CHOICES = (
        ("ToDo", "To DO"),
        ("Doing", "Doing"),
        ("Done", "Done"),
    )
    title = models.CharField(_("Title"), max_length=255)
    created_at = models.DateTimeField(verbose_name=_("Created Date"),
                                      auto_now_add=True)
    description = models.TextField(_("Description"))
    deadline = models.DateTimeField(_("Dead Line"), auto_now=True)
    sprint = models.ForeignKey("projects.Sprint",
                               verbose_name=_("Sprint ID"),
                               on_delete=models.CASCADE,
                               related_name="tasks")
    user = models.ForeignKey("accounts.User",
                             verbose_name=_("User"),
                             null=True,
                             on_delete=models.SET_NULL,
                             related_name="tasks")
    status = models.CharField(_("Status"), choices=CHOICES, max_length=255)

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")

    def __str__(self):
        return self.title

    @classmethod
    def create_task(cls: "Task", title, description, deadline, sprint, user, status):
        task = Task.objects.create(title=title,
                                   description=description,
                                   deadline=deadline,
                                   sprint=sprint,
                                   user=user,
                                   status=status)
        return task
    
    @classmethod
    def get_task(cls: "Task", id):
        task = get_object_or_404(Task, pk=id)
        return task
    

    def update_task(self: "Task", task_id, **kwargs):
        task = Task.get_task(task_id)
        for attr, value in kwargs.items():
            setattr(task, attr, value)
        task.save()

class Label(models.Model):
    name = models.CharField(_("Name"),
                            max_length=255)

    @classmethod
    def create_label(self: "Label", name):
        label = Label.objects.create(name=name)
        return label
    
    @classmethod
    def get_label(self: "Label", id):
        label = get_object_or_404(Label, pk=id)
        return label
    
    class Meta:
        verbose_name = _("Label")
        verbose_name_plural = _("Labels")

    def __str__(self):
        return self.name


class TaskLabel(models.Model):
    label = models.ForeignKey("Label",
                              verbose_name=_("Label"),
                              null=True,
                              on_delete=models.SET_NULL)
    task = models.ForeignKey("Task",
                             verbose_name=_("Task"),
                             null=True, on_delete=models.SET_NULL,
                             related_name="labels")

    @classmethod
    def create_task_label(cls: "TaskLabel", label_id, task_id):
            task_label = cls.objects.create(label=label_id, task=task_id)
            return task_label
    
    @classmethod
    def get_task_label(cls: "TaskLabel", id):
        task_label = get_object_or_404(TaskLabel, pk=id)
        return task_label
    
    def update_task_label(self: "TaskLabel",id, **kwargs);
        task_label = TaskLabel.get_task_label(id)
        for attr, value in kwargs.items():
            setattr(task_label, attr, value)
        task_label.save()

    class Meta:
        verbose_name = _("Task Label")
        verbose_name_plural = _("Task Labels")

    def __str__(self):
        return self.id


class Comment(models.Model):
    content = models.TextField(_("Content"))
    created_at = models.DateTimeField(_("Created Time"),
                                      auto_now_add=True)
    user = models.ForeignKey("accounts.User",
                             verbose_name=_("User"),
                             on_delete=models.CASCADE,
                             related_name="comments")
    task = models.ForeignKey("Task",
                             verbose_name=_("Task"),
                             on_delete=models.CASCADE,
                             related_name="comments")

    @classmethod
    def create_comment(cls: "Comment", content, user_id, task_id):
        comment = cls.objects.create(content=content,
                                     user=user_id,
                                     task=task_id)
        return comment
    
    @classmethod
    def get_comment(cls: "Comment", id):
        comment = get_object_or_404(Comment, pk=id)
        return comment
    
    def update_comment(self: "Comment", id, **kwargs):
        comment = Comment.get_comment(id)
        for attr, value in kwargs.items():
            setattr(comment, attr, value)
        comment.save()

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return self.content


class Attachment(models.Model):
    content = models.FileField(_("Content"),
                               upload_to="task-attachments")
    task = models.ForeignKey("Task",
                             verbose_name=_("Task"),
                             on_delete=models.CASCADE,
                             related_name="attachments")

    class Meta:
        verbose_name = _("Attachment")
        verbose_name_plural = _("Attachments")

    def __str__(self):
        return f"Attachment {self.id}"


class WorkTime(models.Model):
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now=True,
                                    null=True)
    task = models.ForeignKey("Task",
                             verbose_name=_("Task"),
                             on_delete=models.CASCADE,
                             related_name="work_times")

    class Meta:
        verbose_name = _("Work Time")
        verbose_name_plural = _("Work times")

    def __str__(self):
        return f"task: {self.task}, start time: {self.start_date.strftime('%Y - %m - %d')}"
