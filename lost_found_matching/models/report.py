from dataclasses import dataclass
from typing import Optional
@dataclass
class Report:
    report_type: str; item_name: str; description: str = ""; category: str = ""; color: str = ""
    location_name: str = ""; latitude: Optional[float] = None; longitude: Optional[float] = None
    event_date: str = ""; event_time: str = ""; image_path: str = ""; status: str = "ACTIVE"
