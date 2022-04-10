#!/bin/bash

# Stop when one of the servers exits with a non-zero exit code
set -e

export DATABASE_URL=postgresql://postgres:@localhost/postgres
# Tests
source ./backend/env/bin/activate
cd backend
python3 -m pytest -vv app/tests
cd ..

