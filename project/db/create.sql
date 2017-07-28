CREATE DATABASE yelp_us_out;

CREATE TABLE group(
	group_id INT NOT NULL AUTO_INCREMENT,
	group_name VARCHAR(50) NOT NULL,
	member_count INT DEFAULT 0,
	create_date DATETIME DEFAULT CURRENT_TIMESTAMP, 
	update_date DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP, 
	PRIMARY KEY(GroupId)
);

CREATE TABLE group_details(
	group_id INT NOT NULL,
	latitude INT NOT NULL,
	longitude INT NOT NULL,
	radius INT DEFAULT NULL,
	price VARCHAR(20) DEFAULT NULL,
	open_at INT DEFAULT NULL,
	categories VARCHAR(512) DEFAULT NULL
);

CREATE TABLE voting_session(
	voting_session_id INT NOT NULL AUTO_INCREMENT,
	group_id INT NOT NULL,
	voting_status VARCHAR(10),
	#voting_result_id INT DEFAULT NULL, # not sure if we want this
	consensus_reached boolean DEFAULT 0,
	create_date DATETIME DEFAULT CURRENT_TIMESTAMP, 
	update_date DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP, 
	PRIMARY KEY(voting_session_id)
);

