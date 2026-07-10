from django.conf import settings
from django.db import models


class TelegramAccount(models.Model):
    """Класс телеграм аккаунта пользователя.

    Attributes:
    user: Внешний ключ к классу пользователя.
    chat_id (Bigint): Id аккаунта пользователя.
    created_at (DateTime): Дата и время создания.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='telegram_account',
        on_delete=models.CASCADE,
    )
    chat_id = models.BigIntegerField()
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)

    def __str__(self):
        return f'Аккаунт пользователя {self.user}'


class Product(models.Model):
    """Класс карточки/семейства маркетплейса.

    Attributes:
        user: Внешний ключ к классу пользователя.
        root (Bigint): Внешний id страницы маркетплейса.
        name (Str): Название карточки.
        created_at (DateTime): Дата и время создания.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='user_products',
        on_delete=models.CASCADE,
    )
    root = models.BigIntegerField(verbose_name='Внешний id страницы маркетплейса')
    name = models.CharField(verbose_name='Название карточки',max_length=128)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'root'],
                name='unique_user_root_product'
            )
        ]


class ProductItem(models.Model):
    """Класс связи артикула с вариациями товара.

    Attributes:
        product: Внешний ключ к артиклу.
        nm (Bigint): Внешний id маркетплейса.
        name (Str): Название карточки товара.
        is_tracked (Bool): Булево поле проверки отслеживания категории.
        is_alive (Bool): Булево поле проверки существования категории.
    """

    product = models.ForeignKey(
        Product, related_name='items',
        on_delete=models.CASCADE,
    )
    nm = models.BigIntegerField()
    name = models.CharField(
        verbose_name='Название карточки',
        max_length=128,
    )
    is_tracked = models.BooleanField(default=True)
    is_alive = models.BooleanField(default=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'nm'],
                name='unique_product_nm'
            )
        ]


class PriceSnapshot(models.Model):
    """Класс снапшотов размеров товара.

    Attributes:
        item: Внешний ключ к ProductItem.
        option_id (BigInt): Размер товара.
        size_name (Str): Наименование размера. Может быть пустым.
        price (Int): Цена размера товара в копейках. Может быть пустым.
        basic_price (Int): Цена размера без скидки в копейках. Может быть пустым.
        stock (Int): Количество товара на складе.
        rating (Decimal): Рейтинг товара.
        reviews_count (Int): Количество отзывов.
        created_at (DateTime): Дата и время создания.
    """

    item = models.ForeignKey(
        ProductItem,
        related_name='snapshots',
        on_delete=models.CASCADE,
    )
    option_id = models.BigIntegerField(verbose_name='Размер товара')
    size_name = models.CharField(
        verbose_name="Размер",
        max_length=10,
        blank=True,
        default=""
    )
    price = models.IntegerField(
        verbose_name='Цена товара',
        null=True,
        blank=True
    )
    basic_price = models.IntegerField(
        verbose_name='Цена товара без скидки',
        null=True,
        blank=True
    )
    stock = models.IntegerField(verbose_name='Количество товара')
    rating = models.DecimalField(
        verbose_name='Рейтинг размера товара',
        max_digits=2,
        decimal_places=1,
        null=True,
        blank=True
    )
    reviews_count = models.IntegerField(
        verbose_name='Количество отзывов',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)

    def __str__(self):
        return f'{self.item} {self.size_name} @ {self.created_at}'


    class Meta:
        indexes = [
            models.Index(
                fields=['item', 'option_id', 'created_at'],
                name='snapshot_item_opt_date_idx'
            ),
            models.Index(
                fields=['item', 'created_at'],
                name='snapshot_item_date_idx'
            ),
        ]

class Niche(models.Model):
    """Класс ниши товаров.

    Attributes:
        user: Fk на модель User.
        name (Str): Имя ниши.
        products: m2m на модель Product.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='niches',
        on_delete=models.CASCADE
    )
    name = models.CharField(
        verbose_name='Имя ниши',
        max_length=128,
    )
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'],
                name='unique_user_name'
            )
        ]
