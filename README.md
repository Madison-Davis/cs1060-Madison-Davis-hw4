Welcome to HW4!  Here are some notes for graders:

1. "Behavior on bad CSV is undefined" means the script is not required to gracefully handle erroneous or malformed CSV files.  Based on the prompt, my model (GPT-4.1 Harvard Sandbox) chose to not do anything, which is within the specification.
2. How we handle SQL injection: We use ? placeholders and the tuple of values (zip_code,) or (county_name, state_abbr, measure_name) which tells SQLite to treat the input as data, not SQL code.  So it won't execute those values. This automatically prevents SQL injection because the user cannot inject SQL commands through zip_code, county_name, or measure_name.
3. How we handle the queries: We implement the query as two separate queries.  First, we query the zip_county table to get the county and state, then with that we query the county_health_rankings table to get the data.

