from database.db import get_connection
from .entities.Comment import Comment
import logging


class CommentModel():
    @classmethod
    def add_comment(self,comment):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO comments (id, text, date, id_user, id_item,name_user) VALUES (%s,%s,%s,%s,%s,%s) ", 
                    (comment.id,comment.text,comment.date,comment.id_user,comment.id_item,comment.name_user))
                affect_rows=cursor.rowcount
                connection.commit()
            connection.close()
            return affect_rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod     
    def get_comment_by_product_id(self,Id):
            try:
                connection = get_connection()
                comments=[]
                with connection.cursor() as cursor:
                    Id=tuple(map(str, Id.split(', ')))
                    cursor.execute(
                    "SELECT * FROM comments WHERE id_item=%s",(Id))
                    resultset = cursor.fetchall()
                    for row in resultset:
                         comment = Comment(row[0], row[1], row[2], row[3], row[4],row[5])
                         comments.append(comment)
                connection.close()
                return comments
            except Exception as ex:
                raise Exception(ex)
    @classmethod
    def delete_comment(self,Id):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                Id=tuple(map(str, Id.split(', ')))
                cursor.execute("DELETE FROM comments WHERE id =%s", (Id))
                affect_rows=cursor.rowcount
                connection.commit()
            connection.close()
            return affect_rows
        except Exception as ex:
            raise Exception(ex)