from enum import Enum


class CareerLevel(Enum):
    entry_level = "entry level"
    junior = "junior"
    senior = "senior"
    lead = "lead"

class Gender(Enum):
    male = "male"
    female = "female"
    other = "other"

class JobType(Enum):
    internship = "internship"
    full_time = "full-time"
    part_time = "part-time"
    contract = "contract"

class EducationLevel(Enum):
  high_school = "high school"
  bachelor = "bachelor's degree"
  master = "master's degree"
  phd = "Ph.D."

  
class Decision(Enum):
    accepted = "accepted"
    rejected = "rejected"
    pending = "pending"



class Package(Enum):
    basic = "basic"
    standard = "standard"
    extended = "extended"

class LanguageProficiency(Enum):
    A1 = "A1: Breakthrough or Beginner"
    A2 = "A2: Waystage or Beginner Low Intermediate"
    B1 = "B1: Threshold or Intermediate"
    B2 = "B2: Vantage or Upper Intermediate"
    C1 = "C1: Effective Operational Proficiency or Advanced"
    C2 = "C2: Mastery or Proficient"


