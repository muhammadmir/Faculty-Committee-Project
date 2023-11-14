# Faculty Committee Application

## About
This project was an assignment for CSCI 300 under Professor Rudniy. The application idea was initially presented by the Dean's Office. They were interested in a more robust system for viewing information about Faculty, Committees, and the relationship between Faculty and Committees (Relation).

## Technology Used
This backend of the application was built using [Flask](https://flask.palletsprojects.com/en/3.0.x/) and [MySQL Connector for Python](https://dev.mysql.com/doc/connector-python/en/). The frontend was built using [DataTables](https://datatables.net).

A MySQL and low-budget servers are needed to maintain the project.

## Features
This project has three main pages:
1. Faculty Page

    This page enables the viewer to see all the information about Faculty members that are added to the database. Each Faculty member has the following attributes:
    * Name
    * Department
    * Affiliation within Department
    * Title within Department

    Note: Faculty members who belong to multiple Departments will show up multiple times.

2. Committee Page

    This page enables the viewer to see all the information about Committees that are added to the database. Each Committee has the following attributes:
    * Code
    * Name
    * Designation
    * Type

3. Relation Page

    This page enables the viewer to see all the Faculty members and the respective Committees they serve on. We define this relationship as a Relation. Each Relation has the following attributes:
    * Attributes of Faculty
    * Attributes of Committee
    * Serving Period (From what period Faculty will be on Committee)

Each page has functionality to add, edit, or remove an entry. Additionally, each page has filtering and sorting options.

## Setup
An environment file needs to be created to access the MySQL server where data is being stored, retrieved, and uploaded to/from. The `.env` file should contain the following:
```
MYSQL_USER = "username"
MYSQL_PASS = "password"
MYSQL_HOST = "host_address"
MYSQL_DB = "mysql_database_name"
```
The MySQL DB should have the following Tables with the following headers:
1. Faculty
    * FacultyID
    * FacultyName
    * FacultyDepartment
    * Faculty Affiliation
    * FacultyTitle
2. Committee
    * CommitteeID
    * CommitteeCode
    * CommitteeName
    * CommitteeDesignation
    * CommitteeType
3. Relation
    * FacultyName
    * CommitteeCode
    * Serving Period

## To-do List
1. Document Flask code
2. Make front-end prettier