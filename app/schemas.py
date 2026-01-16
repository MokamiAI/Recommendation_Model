from pydantic import BaseModel

class ScrapeResponse(BaseModel):
    total_products: int
    excel_file: str
