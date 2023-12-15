CREATE TYPE user_type AS ENUM ('student', 'teacher');

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role user_type
);
CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    visible BOOLEAN DEFAULT TRUE,
    owner TEXT
);
CREATE TABLE enrollments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    course_id INTEGER REFERENCES courses
);

CREATE TABLE course_materials (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses,
    title TEXT,
    content TEXT
);

CREATE TABLE multiple_choices (
  id SERIAL PRIMARY KEY,
  course_id INTEGER REFERENCES courses,
  question TEXT,
  correct_answer TEXT
);
CREATE TABLE choices (
    id SERIAL PRIMARY KEY,
    multiple_choice_id INTEGER REFERENCES multiple_choices,
    choice TEXT
);

CREATE TABLE text_assignments (
  id SERIAL PRIMARY KEY,
  course_id INTEGER REFERENCES courses,
  question TEXT,
  correct_answer TEXT
);

CREATE TABLE user_correct_choices (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    course_id INTEGER REFERENCES courses,
    multiple_choice_id INTEGER REFERENCES multiple_choices
);

CREATE TABLE user_correct_answers (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    course_id INTEGER REFERENCES courses,
    text_assignment_id INTEGER REFERENCES text_assignments
);
