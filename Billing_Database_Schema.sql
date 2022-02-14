CREATE TABLE `PROJECT_DETAILS` (
  `project_details_id` int PRIMARY KEY AUTO_INCREMENT,
  `project_name` varchar(255),
  `client_name` varchar(255),
  `status_flag` int NOT NULL,
  `commence_date` datetime,
  `duration_inweeks` int
);

CREATE TABLE `WORKSTREAM` (
  `workstream_id` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255)
);

CREATE TABLE `LABOR_CATEGORY` (
  `labor_id` int PRIMARY KEY AUTO_INCREMENT,
  `labor_type` varchar(255),
  `country` varchar(255),
  `cost_per_hour` float4
);

CREATE TABLE `USER` (
  `user_id` int PRIMARY KEY AUTO_INCREMENT,
  `email_id` varchar(255),
  `first_name` varchar(255),
  `last_name` varchar(255),
  `password` char(255),
  `role_id` int,
  `status_type` int
);

CREATE TABLE `ROLE` (
  `role_id` int PRIMARY KEY AUTO_INCREMENT,
  `role_name` varchar(255)
);

CREATE TABLE `PROJECT_BUDGET` (
  `project_budget_id` int PRIMARY KEY AUTO_INCREMENT,
  `project_id` int,
  `prepared_by` int,
  `created_date` timestamp,
  `last_modified_date` timestamp,
  `total_budget` float
);

CREATE TABLE `BUDGET_BREAKDOWN` (
  `budget_breakdown_id` int PRIMARY KEY AUTO_INCREMENT,
  `project_budget_id` int,
  `labor_category_id` int,
  `labor_hours` int,
  `workstream_id` int
);

CREATE TABLE `STATUS_TYPE` (
  `status_type_id` int PRIMARY KEY AUTO_INCREMENT,
  `type` varchar(255)
);

ALTER TABLE `PROJECT_DETAILS` ADD FOREIGN KEY (`status_flag`) REFERENCES `STATUS_TYPE` (`status_type_id`);

ALTER TABLE `USER` ADD FOREIGN KEY (`role_id`) REFERENCES `ROLE` (`role_id`);

ALTER TABLE `USER` ADD FOREIGN KEY (`status_type`) REFERENCES `STATUS_TYPE` (`status_type_id`);

ALTER TABLE `PROJECT_BUDGET` ADD FOREIGN KEY (`project_id`) REFERENCES `PROJECT_DETAILS` (`project_details_id`);

ALTER TABLE `PROJECT_BUDGET` ADD FOREIGN KEY (`prepared_by`) REFERENCES `USER` (`user_id`);

ALTER TABLE `BUDGET_BREAKDOWN` ADD FOREIGN KEY (`project_budget_id`) REFERENCES `PROJECT_BUDGET` (`project_budget_id`);

ALTER TABLE `BUDGET_BREAKDOWN` ADD FOREIGN KEY (`labor_category_id`) REFERENCES `LABOR_CATEGORY` (`labor_id`);

ALTER TABLE `BUDGET_BREAKDOWN` ADD FOREIGN KEY (`workstream_id`) REFERENCES `WORKSTREAM` (`workstream_id`);
