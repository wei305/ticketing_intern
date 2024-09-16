import argparse
import logging

from src.common.config import TixcraftConfig
from src.tixcraft import TixCraft


def main():
    config = build_config()

    app = TixCraft(config)
    app.setup_browser()
    app.close_consent()
    app.login()
    app.execute()


def build_config() -> TixcraftConfig:
    parser = argparse.ArgumentParser(description="Tixcraft part-time worker")

    # Add arguments
    parser.add_argument('--facebook_account', type=str, help='Facebook email or phone (required)', required=True)
    parser.add_argument('--facebook_password', type=str, help='Facebook password (required)', required=True)
    parser.add_argument('--page', type=str, help='Event page to open (required)', required=True)

    # Parse arguments
    args = parser.parse_args()
    return TixcraftConfig(
        target_page=args.page,
        facebook_account=args.facebook_account,
        facebook_password=args.facebook_password,
    )


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    logging.info("Running against tixcraft...")

    main()
