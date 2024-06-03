from typing import List, Optional

from pydantic import EmailStr


from src.schemas.package import PackageOut
from src.schemas.social_links import  SocialLinksCreate, SocialLinksOut
from src.schemas.base_schema import OrmSchema
from src.schemas.contact_info import ContactInfoCreate, ContactInfoOut



class CompanyOut(OrmSchema):
    id: int
    company_name: str|None
    establishment_year: str|None
    team_size: int|None
    description: str|None
    image: str|None
    #jobs: Optional[List["JobOut"]]
    contact_info: ContactInfoOut|None
    social_links: SocialLinksOut|None
    ban_status: str|None
    status: int
    fullname: str
    package: PackageOut|None

class CompanyIn(OrmSchema):  
    id: int

class CompanyCreate(OrmSchema):
    establishment_year: str|None
    team_size: int|None
    description: str|None
    image: str|None
    company_name: str|None
    contact_email: str|None
    contact_info: ContactInfoCreate|None
    social_links: SocialLinksCreate|None
    


