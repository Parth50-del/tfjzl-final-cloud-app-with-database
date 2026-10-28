from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onlinecourse', '0003_alter_choice_id_alter_course_id_alter_enrollment_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='content',
            new_name='question_text',
        ),
        migrations.RenameField(
            model_name='choice',
            old_name='content',
            new_name='choice_text',
        ),
    ]
