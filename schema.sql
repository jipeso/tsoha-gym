CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);
CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    name TEXT
);
CREATE TABLE enrollments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    course_id INTEGER REFERENCES courses
);
CREATE TABLE completions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    completed_at TIMESTAMP
);
CREATE TABLE course_materials (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses,
    content TEXT
);
CREATE TABLE assignments (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses,
    question TEXT,
    type TEXT
);
CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    assignment_id INTEGER REFERENCES assignments,
    text_answer TEXT,
    selected_answer TEXT
);