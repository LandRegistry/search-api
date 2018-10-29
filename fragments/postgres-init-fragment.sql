-- Create search_api_db database
CREATE DATABASE search_api_db;

--Create user for search_api_db DB
CREATE ROLE search_api_db_user with LOGIN password 'password';

\c search_api_db;
CREATE EXTENSION postgis;
