"""Main entrypoint of app."""

import sys
import configparser

import extractor
import db


def read_db_config():
    """Read db connection info from ini file."""
    config = configparser.ConfigParser()
    config.read("db.ini")
    db_cfg = {}
    try:
        db_cfg["database"] = config["CONNECTION"]["database"]
        db_cfg["host"] = config["CONNECTION"]["host"]
        db_cfg["port"] = int(config["CONNECTION"]["port"])
        db_cfg["user"] = config["CONNECTION"]["user"]
        db_cfg["password"] = config["CONNECTION"]["password"]
    except Exception as excp:
        print(f"db.ini error: Missing parameter {excp}")
        return None
    return db_cfg


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_file>")
        sys.exit()
    db_config = read_db_config()
    if not db_config:
        sys.exit()
    interfaces = extractor.extract_ifaces(sys.argv[1])
    db.insert_ifaces(db_config, interfaces)
