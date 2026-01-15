# app/schemas/ingestion.py

from pydantic import BaseModel, HttpUrl, Field


class RawProductIn(BaseModel):
    """
    Raw insurance product payload used by /ingest-raw
    """

    company_name: str = Field(..., example="Sanlam")
    product_name: str = Field(..., example="Life Insurance")
    product_page_url: HttpUrl = Field(
        ...,
        example="https://www.sanlam.co.za/personal/insurance/life-insurance"
    )
    raw_text: str = Field(
        ...,
        example="This product provides life cover. Premiums are payable monthly."
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "company_name": "Sanlam",
                "product_name": "Life Insurance",
                "product_page_url": "https://www.sanlam.co.za/personal/insurance/life-insurance",
                "raw_text": "This product provides life cover. Premiums are payable monthly."
            }
        }
    }
