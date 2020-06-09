from sqlalchemy.orm import Session
# from models.model import EnvModel
# from models.schemas import EnvSchemas
from models import model
from models import schemas


def getEnvs(db: Session, size: int = 0, page: int = 10):
    return db.query(model.Environment).all()


def getEnvs_by_id(db: Session, env_id: int):
    return db.query(model.Environment).filter(model.Environment.id == env_id).first()


def getEnvs_by_name(db: Session, env_name: str):
    return db.query(model.Environment).filter(model.Environment.name == env_name).first()


def createEnv(db: Session, env: schemas.EnvCreate):
    db_env = model.Environment(
        name=env.name,
        content=env.content,
        comment=env.comment,
        path=env.path)
    db.add(db_env)
    db.commit()
    db.close()
    return db_env


def editEnv(db: Session, env_id: int, env: schemas.Env):
    # print(1, template.name)
    db_env = db.query(model.Environment).filter(model.Environment.id == env_id).update({
        'content': env.content,
        'comment': env.comment
    })
    db.commit()
    db.close()
    return db_env


def deleteEnv(db: Session, env_id: int):
    db_env = db.query(model.Environment).filter(model.Environment.id == env_id).first()
    db.delete(db_env)
    db.commit()
    return db_env


def getTemplates(db: Session, size: int = 0, page: int = 10):
    return db.query(model.ServiceTemplate).all()


def getTemplate_by_id(db: Session, template_id: int):
    return db.query(model.ServiceTemplate).filter(model.ServiceTemplate.id == template_id).first()


def getTemplate_by_name(db: Session, template_name: str):
    return db.query(model.ServiceTemplate).filter(model.ServiceTemplate.name == template_name).first()


def createTemplate(db: Session, template: schemas.TemplateCreate):
    db_template = model.ServiceTemplate(
        name=template.name,
        content=template.content,
        comment=template.comment,
        path=template.path)
    db.add(db_template)
    db.commit()
    db.close()
    return db_template


def editTemplate(db: Session, template_id: int, template: schemas.Template):
    print(1, template.name)
    db_template = db.query(model.ServiceTemplate).filter(model.ServiceTemplate.id == template_id).update({
        'content': template.content,
        'comment': template.comment
    })
    db.commit()
    db.close()
    return db_template


def deleteTemplate(db: Session, template_id: int):
    db_template = db.query(model.ServiceTemplate).filter(model.ServiceTemplate.id == template_id).first()
    db.delete(db_template)
    db.commit()
    return db_template


# 通过id查询用户信息
def get_user(db: Session, user_id: int):
    # print(dir(db))
    return db.query(model.User).filter(model.User.id == user_id).first()  # 过滤器


def get_user_by_name(db: Session, username: str):
    return db.query(model.User).filter(model.User.username == username).first()


def del_user(db: Session, username: str):
    db_user = db.query(model.User).filter(model.User.username == username).first()
    db.delete(db_user)
    db.commit()
    return db_user


def update_user(db: Session, user: schemas.UserCreate):
    from core.Base import get_password_hash
    fake_hashed_password = get_password_hash(user.password)
    # print(user.username)
    db_user = db.query(model.User).filter(model.User.username == user.username).update(email=user.email, password=fake_hashed_password, role=user.role)
    # db_user
    # db_user = model.User(email=user.email, password=fake_hashed_password, username=user.username, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# 通过id范围查询用户信息
def get_users(db: Session, skip: int = 0, limit: int = 100):  # 初值末值
    return db.query(model.User).offset(skip).limit(limit).all()


# 新建用户
def create_user(db: Session, user: schemas.UserCreate):
    from core.Base import get_password_hash
    fake_hashed_password = get_password_hash(user.password)
    # print(user.username)
    db_user = model.User(email=user.email, password=fake_hashed_password, username=user.username, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
