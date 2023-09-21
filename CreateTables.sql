CREATE TABLE IF NOT EXISTS Roles(
    `role_id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    `role_name` VARCHAR(25) NOT NULL
);

CREATE TABLE IF NOT EXISTS Majors(
    `major_id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    `major_name` VARCHAR(25) NOT NULL
);

CREATE TABLE IF NOT EXISTS Degrees (
    `degree_id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    `degree_name` VARCHAR(25) NOT NULL
);

CREATE TABLE IF NOT EXISTS Users(
    `user_id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    `user_fname` VARCHAR(25) NOT NULL,
    `user_lname` VARCHAR(25) NOT NULL,
    `user_email` VARCHAR(25) NOT NULL,
    `role` INTEGER NOT NULL,
    `major` INTEGER NOT NULL,
    `degree` INTEGER NOT NULL,
    `gpa` DECIMAL(3, 2),
    `hours` DECIMAL(5, 2),
    `graduating_semseter` INTEGER,
    FOREIGN KEY (`role`) 
        REFERENCES Roles (`role_id`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
    FOREIGN KEY (`major`)
        REFERENCES Majors (`major_id`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
    FOREIGN KEY (`degree`)
        REFERENCES Degrees (`degree_id`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS Courses(
    `course_id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    `course_name` VARCHAR(25) NOT NULL
);

CREATE TABLE IF NOT EXISTS Jobs(
    `job_id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    `job_name` VARCHAR(25) NOT NULL,
    `course_required` INTEGER,
    `certification_required` BOOL NOT NULL, 
    `status` BOOL NOT NULL,
    FOREIGN KEY (`course_required`)
        REFERENCES Courses (`course_id`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS Certifications(
    `cert_id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    `user_id` INTEGER NOT NULL,
    FOREIGN KEY (`user_id`) 
        REFERENCES Users (`user_id`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS UserCourses(
    `uc_id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    `user_id` INTEGER NOT NULL,
    `course_id` INTEGER NOT NULL,
    `grade` DECIMAL(5,2) NOT NULL,
    FOREIGN KEY (`user_id`)
        REFERENCES Users (`user_id`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
    FOREIGN KEY (`course_id`)
        REFERENCES Courses (`course_id`)
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS Applications(
    `app_id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    `user_id` INTEGER NOT NULL,
    `course_id` INTEGER NOT NULL,
    `status` BOOL NOT NULL,
    `editable` BOOL NOT NULL,
    FOREIGN KEY (`user_id`)
        REFERENCES Users (`user_id`)
            ON UPDATE NO ACTION
            ON DELETE NO ACTION,
    FOREIGN KEY (`course_id`)
        REFERENCES Courses (`course_id`)
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
);
