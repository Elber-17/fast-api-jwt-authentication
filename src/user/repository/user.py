from sqlalchemy.orm import Session

from src.user.models import User
from src.user.schemas.user import UserFindCondition


class UserRepository:
    def find(self, db: Session, condition: UserFindCondition):
        return db.query(User).filter_by(
            **condition.dict(exclude_unset=True, by_alias=False)
        )

    def findOne(self, db: Session, condition: UserFindCondition):
        return (
            db.query(User)
            .filter_by(**condition.dict(exclude_unset=True, by_alias=False))
            .first()
        )

    def findById(self, db: Session, user_id: int):
        return db.query(User).filter(User.id_ == user_id).first()
