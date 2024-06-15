createDatabaseQuery = """CREATE OR REPLACE FUNCTION create_image_features_table() RETURNS void AS $$
BEGIN
    CREATE TABLE IF NOT EXISTS image_features (
        id SERIAL PRIMARY KEY,
        image_name TEXT NOT NULL,
        image_url TEXT NOT NULL,
        image_hash TEXT NOT NULL,
        image_feature FLOAT8[] NOT NULL
    );
END;
$$ LANGUAGE plpgsql;"""

testConnectionQuery = """CREATE OR REPLACE FUNCTION test_connection() RETURNS TABLE (version TEXT, version_number TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT version() AS version, current_setting('server_version_num') AS version_number;
END;
$$ LANGUAGE plpgsql;"""

createSchemaQuery = """CREATE OR REPLACE FUNCTION create_schema() RETURNS void AS $$
BEGIN
    CREATE SCHEMA IF NOT EXISTS ClearView;
END
$$ LANGUAGE plpgsql;
"""