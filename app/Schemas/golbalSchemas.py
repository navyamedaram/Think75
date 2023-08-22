from enum import Enum
class userStatusEnum(str, Enum):
    "User Status Enum"
    active = "active"
    inactive = "inactive"
    blocked = "blocked"
    deleted = "deleted"
class difficultyEnum(str, Enum):
    "User Status Enum"
    easy = "easy"
    medium = "medium"
    hard = "hard" 