import streamlit as st
import json

if 'Logged_in' not in st.session_state:
    st.session_state['Logged_in'] = False

if not st.session_state["Logged_in"]:

    st.title("Feel-Blog")
    st.header("Login/Registration")

    username = st.text_input("Username")
    password = st.text_input("Password" , type="password")


#login
    if st.button("Login"):
        with open('users.json','r') as file:
            users = json.load(file)

        Login_success = False
        for user in users:
            if user['username'] == username and user['password'] == password:
                Login_success = True
                break

        if Login_success:
            st.success("Login successful")
            st.session_state["Logged_in"] = True
            st.session_state['username'] = username
        else:
            st.error("Invalid username or password")


    #register
    if st.button("Register"):
        with open('users.json','r') as file:
            users = json.load(file)

        if username in [user['username'] for user in users]:
            st.error("username already exists")
        else:
            users.append({
                'username':username,
                'password':password
            })

            with open('users.json','w') as file:
                json.dump(users,file)

            st.success("Register Successfull")

# new page / blog page

if st.session_state['Logged_in']:


    st.title("Welcome to Feel Blog")

    name = st.text_input("Your name")
    title = st.text_input("Title")
    blog = st.text_area("Your Blog")
    # file uploaded
    image_file = st.file_uploader(label="upload your image",type=["jpg", "jpeg", "png"])
    # pdf_file = st.file_uploader(label="upload your pdf",type=["pdf"])


    #___________________________________________________

    if st.button("Publish"):
        with open('blogs.json','r') as file:
            blogs = json.load(file)

        image_path = None
        # pdf_path = None

        if image_file:
            image_path = 'images/' + image_file.name

            with open(image_path, 'wb') as file:
                file.write(image_file.getbuffer())
        #
        # #pdf file
        # if pdf_file:
        #     pdf_path = "pdf/" + pdf_file.name
        #
        #     with open(pdf_path,'wb') as file:
        #         file.write(pdf_file.getbuffer())

        # ___________________________________________________
        blogs.append({
            'username':st.session_state['username'],
            'name':name,
            'title':title.upper(),
            'blog':blog,
            'image':image_path
            # 'pdf':pdf_path
        })

        with open('blogs.json','w') as file:
            json.dump(blogs,file)

        st.success("Blog Published")


    # blog displying
    with open('blogs.json','r') as file:
        blogs = json.load(file)

        for blog in blogs:
            st.header(blog['title'])
            st.write("By:",blog['name'])
            st.write(blog['blog'])
            if blog.get('image'):
                st.image(blog['image'],width=350,)
            # if blog.get('pdf'):
            #     st.pdf(blog['pdf'])
            st.divider()

    # logout
    if st.button('Logout'):
        st.session_state['Logged_in'] = False
        st.session_state['username'] = ""
        st.rerun()














