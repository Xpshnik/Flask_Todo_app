from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import Length, DataRequired, ValidationError


class TodoForm(FlaskForm):
    task_name = StringField('Task name',
                            validators=[DataRequired('Try being more eloquent ;)'), Length(min=3, max=300)])
    is_urgent = BooleanField('Is urgent?')
    submit = SubmitField('Add')

    def validate_task_name(form, field):
        if 'tomorrow' in field.data.lower():
            raise ValidationError("Yesterday you said 'tomorrow', so just do it!")
