from dataclasses import dataclass


@dataclass
class StartupInfo:
    company: str
    country: str
    sector: str
    funding: int
    source_url: str

    def is_valid(self) -> bool:
        if not self.company or not self.company.strip():
            return False

        if not self.country or self.country.strip().lower() == "unknown":
            return False

        if not self.sector or self.sector.strip().lower() == "unknown":
            return False

        if self.funding < 0:
            return False

        return True