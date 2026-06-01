from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Shop:
    name: str
    months_values: list[float]

    id: UUID = field(default_factory=uuid4)

    @property
    def total_per_year(self) -> float:
        return sum(self.months_values, 0.0)

    @property
    def max_consumption(self) -> float:
        return max(self.months_values, default=0.0)

    @property
    def max_consumption_month_index(self) -> int | None:
        max_val = self.max_consumption
        if max_val == 0.0:
            return None
        return self.months_values.index(max_val)
