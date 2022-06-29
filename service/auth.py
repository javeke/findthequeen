from data import data_store

def validate_credentials(username, password):
  for user in data_store.users:
    if user["username"] == username and user["password"] == password:
      return True
  return False