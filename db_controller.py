from models.db_model import User, Rights, UserRights
from playhouse.shortcuts import model_to_dict


# Create a new user with rights
def create_user(name, age, gender='M', rights=None):
    user = User(name=name, age=age, gender=gender)
    user.save()

    if rights:
        for right in rights:
            right_obj, created = Rights.get_or_create(right=right)
            UserRights.create(user=user, right=right_obj)

    return user.id  # return the ID of the created user


# Retrieve all users with their rights
def get_all_users():
    users = User.select()
    users_with_rights = []
    for user in users:
        user_dict = model_to_dict(user)
        user_dict['rights'] = [user_right.right.right for user_right in user.rights]
        users_with_rights.append(user_dict)
    return users_with_rights


# Retrieve a user by ID with their rights
def get_user_by_id(user_id):
    try:
        user = User.get_by_id(user_id)
        user_dict = model_to_dict(user)
        user_dict['rights'] = [user_right.right.right for user_right in user.rights]
        return user_dict
    except User.DoesNotExist:
        return None


# Update user and their rights
def update_user(user_id, name=None, age=None, rights=None):
    user = User.get_by_id(user_id)
    if user:
        if name:
            user.name = name
        if age:
            user.age = age
        if rights:
            UserRights.delete().where(UserRights.user == user).execute()  # delete old rights
            for right in rights:  # add new rights
                right_obj, created = Rights.get_or_create(right=right)
                UserRights.create(user=user, right=right_obj)
        user.save()


# Delete user and their rights
def delete_user(user_id):
    user = User.get_by_id(user_id)
    if user:
        UserRights.delete().where(UserRights.user == user).execute()  # delete associated rights
        user.delete_instance()
