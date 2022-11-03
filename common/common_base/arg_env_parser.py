import argparse
import os

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    pass


def parse_args_env(kw_args_env):
    """
    Example:
        kw_args_env = {
            "kw_name": {
                "args": ["--arg-name", "-a"],
                "env": "VAR_NAME"
            }
        }
        kw_values = parse_args_env(kw_args_env)
        print(kw_values)  # { "kw_name": "value" }
    """

    if "load_dotenv" in globals():
        if os.path.exists('envvars'):
            load_dotenv('envvars')
        elif os.path.exists('.env'):
            load_dotenv('.env')

    parser = argparse.ArgumentParser()
    for v in kw_args_env.values():
        parser.add_argument(*v["args"])

    # args_values = vars(parser.parse_args())
    (known_args_values, _) = parser.parse_known_args()
    args_values = vars(known_args_values)

    kw_values = {}
    for (kw, v) in kw_args_env.items():
        arg = v["args"][0].replace('--', '').replace('-', '_')
        env_var = v["env"]
        value = args_values[arg] or os.environ.get(env_var)
        kw_values[kw] = value

    return kw_values


if __name__ == "__main__":
    # example only
    kw_args_env = {
        "kw_name": {
            "args": ["--arg-name", "-a"],
            "env": "VAR_NAME"
        }
    }
    kw_values = parse_args_env(kw_args_env)
    print(kw_values)  # { "kw_name": "value" }
