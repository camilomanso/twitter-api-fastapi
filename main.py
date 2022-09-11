# Python
from genericpath import exists
from uuid import UUID
from datetime import date
from datetime import datetime
from typing import Optional, List
import json

# Pydantic
from uuid import UUID
from pydantic import BaseModel, Field
from pydantic import EmailStr

# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body, Path, HTTPException, Form

app = FastAPI()

# Models

class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)

class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )

class User(UserBase):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    birth_date: Optional[date] = Field(default=None)

class UserRegister(User):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )

class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ...,
        min_length=1,
        max_length=256
    )
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    by: User = Field(...)

# Aditional function 

def read_data(file):
    with open(f"{file}.json", "r+", encoding="utf-8") as f:
        return json.loads(f.read()) # Convertirlo a simil de json

def overwrite_data(file, results):
    with open(f"{file}.json", "w", encoding="utf-8") as f:
        f.seek(0)  # Moverte al inicio del archivo
        f.write(json.dumps(results))  # Convirtiendo de una list_dic a un json

def show_data(file, id, info):
    results = read_data(file)
    id = str(id)
    for data in results:
        if data[f"{info}_id"] == id:
            return data
    else:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= f"¡This {info} doesn't exist!"

        )

def delete_data(file, id, info):
    results = read_data(file)
    id = str(id)
    for data in results:
        if data[f"{info}_id"] == id:
            results.remove(data)
            overwrite_data(file,results)
            return data
    else:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= f"¡This {info} doesn't exist!"

        )

# Path Operations

## Users

### Register a user
@app.post(
    path="/signup",
    response_model=User,
    status_code= status.HTTP_201_CREATED,
    summary= "Register a User",
    tags=["Users"]
)
def signup(user: UserRegister = Body(...)):
    """
    Signup
    
    This path operation register a user in the app

    Parameters:
        -Request body parameter
            -user: UserRegister
    
    Returns a json with the basic user information:
        -user_id: UUID
        -email: EmailStr
        -first_name: str
        -last_name: str
        -birth_date: datetime

    """
    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return user

### Login a user
@app.post(
    path="/login",
    response_model=User,
    status_code= status.HTTP_200_OK,
    summary= "Login a User",
    tags=["Users"]
)
def login():
    pass

### Show all users
@app.get(
    path="/users",
    response_model= List[User],
    status_code= status.HTTP_200_OK,
    summary= "Show all users",
    tags=["Users"]
)
def show_all_users():
    """
    Show all users
    
    This path operation shows all users in the app

    Parameters:
        -

    Returns a json list with all users in the app, with the following keys:
        -user_id: UUID
        -email: EmailStr
        -first_name: str
        -last_name: str
        -birth_date: datetime
    
    """
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results

### Show a user
@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code= status.HTTP_200_OK,
    summary= "Show all users",
    tags=["Users"]
)
def show_a_user():
    pass

### Delete a user
@app.delete(
    path="/users/{user_id}/delete",
    response_model=User,
    status_code= status.HTTP_200_OK,
    summary= "Delete a User",
    tags=["Users"]
)
def delete_a_user():
    pass

### Update a user
@app.put(
    path="/users/{user_id}/update",
    response_model=User,
    status_code= status.HTTP_200_OK,
    summary= "Update a User",
    tags=["Users"]
)
def update_a_user():
    pass

## Tweets

### Show all tweets
@app.get(
    path="/",
    response_model= List[Tweet],
    status_code= status.HTTP_200_OK,
    summary= "Show all tweets",
    tags=["Tweets"]    
)
def home():
    """
    Show all tweets
    
    This path operation shows all tweets in the app

    Parameters:
        -

    Returns a json list with all tweets in the app, with the following keys:
        - tweet_id: UUID 
        - content: str 
        - created_at: datetime 
        - updated_at: Optional[datetime] 
        - by: User 
    
    """
    
    return read_data("tweets")

### Post a tweet
@app.post(
    path="/post",
    response_model= Tweet,
    status_code= status.HTTP_201_CREATED,
    summary= "Post a tweet",
    tags=["Tweets"]
)
def post(tweet: Tweet = Body(...)):
    """
    Post a Tweet
    
    This path operation post a tweet in the app

    Parameters:
        -Request body parameter
            -tweet: Tweet
    
    Returns a json with the basic tweet information:
        -tweet_id: UUID
        -content: str
        -created_at: datetime
        -updated_at: Optional[datetime]
        -by: User
         
    """
    
    results = read_data("tweets")
    tweet_dict = tweet.dict()
    tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
    tweet_dict["created_at"] = str(tweet_dict["created_at"])
    tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
    tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"])
    tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"])
    results.append(tweet_dict)
    overwrite_data("tweets", results)
    return tweet

### Show a tweet
@app.get(
    path="/tweets/{tweet_id}",
    response_model= Tweet,
    status_code= status.HTTP_200_OK,
    summary= "Show a tweet",
    tags=["Tweets"]
)
def show_a_tweet(tweet_id: UUID = Path(
    ...,
    title="Tweet ID",
    description="This is the tweet ID"    
    )):
    """
    Show a tweet
    
    This path operation show if a tweet exist in the app

    Parameters:
        - tweet_id: UUID

    Returns a json with tweet data:
        - tweet_id: UUID 
        - content: str 
        - created_at: datetime 
        - updated_at: Optional[datetime] 
        - by: User 
    
    """
    return show_data("tweets", tweet_id, "tweet")

### Delete a tweet
@app.delete(
    path="/tweets/{tweet_id}/delete",
    response_model= Tweet,
    status_code= status.HTTP_200_OK,
    summary= "Delete a tweet",
    tags=["Tweets"]
)
def delete_a_tweet(tweet_id: UUID = Path(
    ...,
    title="Tweet ID",
    description="This is the tweet ID"    
    )):
    """
    Delete a tweet
    
    This path operation delete a tweet in the app

    Parameters:
        - tweet_id: UUID

    Returns a json with tweet data:
        - tweet_id: UUID 
        - content: str 
        - created_at: datetime 
        - updated_at: Optional[datetime] 
        - by: User 
    
    """
    return delete_data("tweets", tweet_id, "tweet")

### Update a tweet
@app.put(
    path="/tweets/{tweet_id}/update",
    response_model= Tweet,
    status_code= status.HTTP_200_OK,
    summary= "Update a tweet",
    tags=["Tweets"]
)
def update_a_tweet(
    tweet_id: UUID = Path(
        ...,
        title="Tweet ID",
        description="This is the tweet ID"    
        ),
    content: str = Form(
        ...,
        min_length=1,
        max_length=256,
        title="Tweet content",
        description="This is the update content of the tweet"
    )
):
    """
    Update a tweet
    
    This path operation update a tweet information in the app and save in the database

    Parameters:
        - tweet_id: UUID
        - content: str

    Returns a json with tweet data:
        - tweet_id: UUID 
        - content: str 
        - created_at: datetime 
        - updated_at: Optional[datetime] 
        - by: User 
    
    """
    tweet_id = str(tweet_id)
    results = read_data("tweets")
    for tweet in results:
        if tweet['tweet_id'] == tweet_id:
            tweet['content'] = content
            tweet['updated_at'] = str(datetime.now())
            print(tweet)
            overwrite_data("tweets", results)
            return tweet
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This tweet doesn't exist!"
        )


