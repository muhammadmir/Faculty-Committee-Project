# Faculty Committee Application

## About
This project was an assignment for CSCI 300 under Professor Rudniy. The application idea was initially presented by the Dean's Office. They were interested in a more robust system for viewing information about Faculty, Committees, and the relationship between Faculty and Committees (Relation).

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
