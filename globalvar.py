def initialize():
    global ismain
    ismain = False

    global isloggedin
    isloggedin = 0


def logged_user():
    global isloggedin
    isloggedin = 1

    global email
    email = ''

    global uploaded_files
    uploaded_files = []

    global selected_image_path
    selected_image_path = ''

    global y_pred
    y_pred = []
