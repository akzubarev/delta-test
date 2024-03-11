from django.db import models


# Посылки бывают 3х типов: одежда, электроника, разное.
# Типы должны храниться в отдельной таблице в базе данных.
class ParcelType(models.Model):
    # тз не описано должна ли быть возможность создавать новые типы
    # без миграций, поэтому, использование choiceField отключено, но если оно
    # имелось в виду - то вот показываю что оно есть
    class TypeNames(models.TextChoices):
        OTHER = 'Разное'
        CLOTHES = 'Одежда'
        ELECTRO = 'Электроника'

    name = models.CharField(
        max_length=20,
        # choices=TypeNames.choices,
        # default=TypeNames.OTHER,
    )
