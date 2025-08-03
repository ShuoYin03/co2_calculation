from typing import Optional
from pydantic import BaseModel, Field, field_validator

ENERGY_TYPE_TO_OPTION_VALUE = {
    "EL": "8",  # Électricité (EL), Hydrogène (H2) ou combinaison des 2 (HE, HH)
    "EH": "16", # Essence/électricité - hybride non rechargeable (EH)
    "ES": "1",  # Essence (ES)
    "GO": "2",  # Gazole (GO), Biogazole B100 (BL)
    "EE": "3",  # Essence/électricité - hybride rechargeable (EE)
    "GL": "12", # Gazole/électricité, Biogazole/électricité - hybride rechargeable (GL, BL)
    "GH": "13", # Gazole/électricité, Biogazole/électricité - hybride non rechargeable (GH, BH)
}

class CalculateTaxRequest(BaseModel):
    registration: str = Field(..., description="First date of vehicle registration, format mm/yyyy")
    power: int = Field(..., description="Vehicle power in kilowatts")
    emission: int = Field(..., description="CO₂ emission in g/km")
    energy: str = Field(..., description="Energy source code")
    weight: int = Field(..., description="Vehicle weight in kg")
    region: int = Field(..., description="Region of the user")
    price: Optional[float] = Field(None, description="Price before tax (optional)")

    @field_validator("registration")
    def registration_format(cls, v):
        import re
        if not re.match(r"^(0[1-9]|1[0-2])/[12]\d{3}$", v):
            raise ValueError("registration must be in mm/yyyy format")
        return v

    @field_validator("energy")
    def energy_code_valid(cls, v):
        if v not in ENERGY_TYPE_TO_OPTION_VALUE.keys():
            raise ValueError(f"energy must be one of {list(ENERGY_TYPE_TO_OPTION_VALUE.keys())}")
        return ENERGY_TYPE_TO_OPTION_VALUE[v]

class CalculateTaxResponse(BaseModel):
    tax_amount: float = Field(..., description="Calculated CO₂ tax, in euros")
    total_price: Optional[float] = Field(None, description="Total price including tax, if price is provided")