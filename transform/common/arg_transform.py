from common_base.arg_env_parser import parse_args_env


def get_transform_args(input_csv, output_dest):
    if input_csv == None:
        kwargs = parse_args_env({
            "input_csv": {
                "args": ["--input-csv", "-i"],
                "env": "INPUT_CSV_TRANSFORM"
            },
        })
        input_csv = kwargs["input_csv"]

    if output_dest == None:
        kwargs = parse_args_env({
            "output_dest": {
                "args": ["--output-dest", "-o"],
                "env": "OUTPUT_DEST_TRANSFORM"
            },
        })
        output_dest = kwargs["output_dest"]

    assert input_csv != None, "missing input_csv"
    assert output_dest != None, "missing output_dest"

    return (input_csv, output_dest)
