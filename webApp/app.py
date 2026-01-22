from webApp import webapp


if __name__ == "__main__":
    app = webapp()
    app.run(host="0.0.0.0", debug=True)