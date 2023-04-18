from ForumApp import new_app
import argparse

app = new_app()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CSE 160 Final Project: Forum Webapp")
    parser.add_argument("--port", default=5000, type=int)
    args = parser.parse_args()

    app.run(host="0.0.0.0", port=args.port, debug = True)  