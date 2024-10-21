import os

# 如何设置环境变量？
# export AG_ENV=prod

def get_env():
    env = os.getenv("AG_ENV")
    print(env)
    return env