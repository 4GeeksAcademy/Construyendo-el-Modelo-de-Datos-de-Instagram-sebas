from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


# 1) USUARIO



class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(30), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False)

    # Relaciones 
    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active,
        }


# 2) POST (publicación)



class Post(db.Model):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        db.ForeignKey("user.id"), nullable=False)
    caption: Mapped[str | None] = mapped_column(
        Text, nullable=True)  
    image_url: Mapped[str] = mapped_column(
        String(255), nullable=False)  

    # Relaciones
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    likes = relationship("Like", back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "caption": self.caption,
            "image_url": self.image_url,
            "comments_count": len(self.comments),
            "likes_count": len(self.likes),
        }


# 3) COMMENT (comentario)



class Comment(db.Model):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        db.ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(
        db.ForeignKey("post.id"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # Relaciones
    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "content": self.content,
        }


# 4) LIKE (me gusta)



class Like(db.Model):
    __tablename__ = "like"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        db.ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(
        db.ForeignKey("post.id"), nullable=False)

    # Relaciones sencillas para navegar
    user = relationship("User")
    post = relationship("Post", back_populates="likes")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id,
        }

# 5) FOLLOW (seguidores)




class Follow(db.Model):
    __tablename__ = "follow"

    id: Mapped[int] = mapped_column(primary_key=True)
    follower_id: Mapped[int] = mapped_column(
        db.ForeignKey("user.id"), nullable=False)  # quién sigue
    followed_id: Mapped[int] = mapped_column(
        db.ForeignKey("user.id"), nullable=False)  # a quién sigue

    follower = relationship("User", foreign_keys=[follower_id])
    followed = relationship("User", foreign_keys=[followed_id])

    def serialize(self):
        return {
            "id": self.id,
            "follower_id": self.follower_id,
            "followed_id": self.followed_id,
        }
