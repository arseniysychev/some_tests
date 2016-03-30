from django.db import models


class Some2(models.Model):
    field1 = models.CharField(max_length=255, default='bbb')


class Some1(models.Model):
    field1 = models.CharField(max_length=255, default='aaa', verbose_name='Field')
    int_field = models.IntegerField()
    date = models.DateTimeField(blank=True, null=True)
    # foreign = models.ForeignKey(Some2, blank=True, null=True)
    m_to_m = models.ManyToManyField(Some2, verbose_name="Many to many field", blank=True)

    def field_convert_to_string(self, field):
        value = getattr(self, field)
        a = type(field)
        b = field.get_internal_type()
        if isinstance(field, models.DateTimeField):
            pass
        return value

    def __unicode__(self):
        return {
            key: str(getattr(self, key)) for key in self.__dict__ if
            not key.startswith('_')
            }.__str__()

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse

        return reverse('app1:some1_detail', kwargs={'pk': self.id})

    class Meta:
        ordering = ["int_field"]
        verbose_name = '_Some_'
        verbose_name_plural = '__SomeS__'
