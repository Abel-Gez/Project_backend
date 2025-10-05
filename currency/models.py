from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator

class ExchangeRate(models.Model):
    """
    Stores one rate row for a base currency (e.g. ETB), currency code (USD),
    and effective_date. buying and selling use Decimal for correct precision.
    """
    base_currency = models.CharField(max_length=10, default='ETB', db_index=True)
    currency = models.CharField(max_length=10, db_index=True)  # e.g. USD, EUR
    effective_date = models.DateField(db_index=True)

    # Precision: e.g. 141.5713 — allow up to 12 digits total and 6 decimals
    buying = models.DecimalField(
        max_digits=12,
        decimal_places=6,
        validators=[MinValueValidator(Decimal('0.000001'))]
    )
    selling = models.DecimalField(
        max_digits=12,
        decimal_places=6,
        validators=[MinValueValidator(Decimal('0.000001'))]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Exchange Rate"
        verbose_name_plural = "Exchange Rates"
        # enforce uniqueness: one rate per base_currency + currency + date
        unique_together = (('base_currency', 'currency', 'effective_date'),)
        ordering = ['-effective_date', 'currency']

    def __str__(self):
        return f"{self.base_currency}/{self.currency} @ {self.effective_date} (buy {self.buying} sell {self.selling})"
