class ConsumptionFormatter:
    @staticmethod
    def parse_csv_value(value: str, default: float = 0.0) -> float:
        if not value:
            return default
        try:
            return float(value.replace(",", "."))
        except ValueError:
            return default

    @staticmethod
    def format_value(value: float) -> str:
        return f"{value:.2f}".replace(".", ",")

    @staticmethod
    def format_values(values: list[float]) -> list[str]:
        return [ConsumptionFormatter.format_value(val) for val in values]
