from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()


class Post_Val(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{
    "title": "title -p1",
    "content": "content -p1",
    "id": 1
}, {
    "title": "title -p2",
    "content": "content -p2",
    "id": 2
}]


def findIndex(int: id):
    index = 0
    for p in my_posts:
        if id == p["id"]:
            index = p["id"]
    return index


# reguest Get method url: "/"
# routes work top down latest has to be in front of by_id in order for the api to use it
@app.get("/")
def root():
    return {"message:"
            "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return {"data": post}


@app.get("/posts/{id}")
def get_post_by_id(id: int, response: Response):
    for p in my_posts:
        if id == p["id"]:
            return {"data": p}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'post with ID = {id} not found')


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createpost(new_post: Post_Val):
    post_dict = new_post.dict()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


#title str, content str,
@app.delete("/posts/{id}")
def deletepost(id: int):
    for p in my_posts:
        if id == p["id"]:
            my_posts.remove(p)
        else:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                                detail=f"post with ID {id} does not exist")


@app.put("/posts/{id}")
def updatepost(id: int, update_post: Post_Val):

    up_post = update_post.dict()
    index = findIndex(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                            detail=f"post with ID {id} does not exist")
    up_post["id"] = id
    my_posts[index] = up_post
    return {"message": "update successful"}
