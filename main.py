import argparse
import sys
from pathlib import Path


def get_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        "colab-config-s3-rclone",
        description="Helps set up S3 credentials in a Google Colab notebook for syncing data to S3.",
    )
    parser.add_argument("-t", "--home-dir", default="/root")
    parser.add_argument("-i", "--aws-key-id")
    parser.add_argument("-s", "--aws-secret-key")
    parser.add_argument("-b", "--bucket", required=False)

    return parser


def write_aws_credentials(
    *, home_dir: str, aws_key_id: str, aws_secret_key: str
) -> None:
    aws_config_path = f"{home_dir}/.aws"
    aws_credentials_file = f"{aws_config_path}/credentials"
    Path(aws_config_path).mkdir(parents=True, exist_ok=True)
    with open(aws_credentials_file, "w") as f:
        f.write("[default]\n")
        f.write(f"aws_access_key_id = {aws_key_id}\n")
        f.write(f"aws_secret_access_key = {aws_secret_key}\n")

    Path(aws_credentials_file).chmod(0o600)

    print(f"wrote aws credentials to {aws_credentials_file}")


RCLONE_CONFIG = """[mys3]
type = s3
provider = AWS
env_auth = true
region = us-east-1
no_check_bucket = true
"""


def write_rclone_config(*, home_dir: str) -> None:
    rclone_config_path = f"{home_dir}/.config/rclone"
    Path(rclone_config_path).mkdir(parents=True, exist_ok=True)

    with open(f"{rclone_config_path}/rclone.conf", "w") as f:
        f.write(RCLONE_CONFIG)

    print(f"wrote rclone config to {rclone_config_path}/rclone.conf")


def bucket_name_to_shell_config(*, home_dir: str, bucket: str) -> None:
    if bucket is not None:
        updated_env_files = []

        env_file = f"{home_dir}/.bashrc"
        if Path(env_file).exists():
            with open(env_file, "a") as f:
                f.write("\n\n# MY S3 BUCKET FOR SYNCING\n")
                f.write(f'export MY_BUCKET="{bucket}"\n\n')

                f.write("# Ensure `rclone copy ./file mys3://$MY_BUCKET/prefix/` succeeds without s3:CreateBucket permission\n")
                f.write("export RCLONE_S3_NO_CHECK_BUCKET=true\n\n")
            updated_env_files.append(env_file)

        if len(updated_env_files):
            print(f'env files updated with BUCKET_NAME="{bucket}":')
            for env_file in updated_env_files:
                print(f"    {env_file}")
        else:
            print("not env files were updated")


def main(argv: list[str]) -> int:
    arg_parser = get_arg_parser()
    parsed = arg_parser.parse_args(argv[1:])
    home_dir = parsed.home_dir
    aws_key_id = parsed.aws_key_id
    aws_secret_key = parsed.aws_secret_key
    bucket = parsed.bucket

    if not Path(home_dir).exists():
        print(f'home dir does not exist: "{home_dir}"')
        return -1

    if aws_key_id is None or aws_secret_key is None:
        arg_parser.print_help()
        return -1

    write_aws_credentials(
        home_dir=home_dir, aws_key_id=aws_key_id, aws_secret_key=aws_secret_key
    )

    write_rclone_config(home_dir=home_dir)

    bucket_name_to_shell_config(home_dir=home_dir, bucket=bucket)

    print("\ndone\n")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
