from django.template import loader
from django.template.context import Context

from email_sender import HTMLEmail


class DjangoHTMLEmail(HTMLEmail):
    def formatting(self, template, context):
        t = loader.get_template(template)
        return t.render(Context(context))
