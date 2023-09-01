import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
      description='runner',
      epilog="That's all folks"
    )

    parser.add_argument('-t', '--target',
                          type=str)

    try:
        args = parser.parse_args()
    except SystemExit:
        sys.exit()


if __name__ == "__main__":
    main()
