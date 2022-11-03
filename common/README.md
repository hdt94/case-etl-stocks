`common_base/arg_env_parser.py` parses script arguments defined whether through command-line arguments or environment variables:
- Use Python 3.6+
- Installing `requirements.common_base.txt` is required for defining parameters through environment variables

```bash
python3 common_base/arg_env_parser.py --arg-name custom_value
VAR_NAME=custom_value python3 common_base/arg_env_parser.py
```
