import argparse
import concurrent.futures
import logging
import time

from src.common.config import TixcraftConfig
from src.tixcraft import TixCraft


def main(config):
    app = TixCraft(config)
    app.setup_browser()
    app.close_consent()
    app.login()
    app.execute()


def build_config() -> TixcraftConfig:
    parser = argparse.ArgumentParser(description="Ticketing intern")

    # Add arguments
    parser.add_argument('--facebook_account', type=str, help='Facebook email or phone (required)', required=True)
    parser.add_argument('--facebook_password', type=str, help='Facebook password (required)', required=True)
    parser.add_argument('--page', type=str, help='Event page to open (required)', required=True)
    parser.add_argument('--num_of_interns', type=int, help='How many interns would you hire (default: 1)', default=1)

    # Parse arguments
    args = parser.parse_args()
    return TixcraftConfig(
        target_page=args.page,
        facebook_account=args.facebook_account,
        facebook_password=args.facebook_password,
        num_of_interns=args.num_of_interns,
    )


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    logging.info("Running against tixcraft...")

    config = build_config()
    with concurrent.futures.ThreadPoolExecutor(max_workers=config.num_of_interns) as executor:
        futures = []
        for i in range(config.num_of_interns):
            future = executor.submit(main, config)
            futures.append(future)
            time.sleep(3)

        for future in concurrent.futures.as_completed(futures):
            future.result()
